"""Visualizador e baixador seletivo de mídias públicas de perfis Fatal Model.

Instale: py -m pip install playwright requests pillow
         py -m playwright install chromium
Execute: py media_profile_downloader.py

O navegador abre sem login automatizado. Navegue até a galeria de mídias antes
de clicar em "Carregar galeria". O programa não contorna bloqueios, DRM ou paywalls.
"""

from __future__ import annotations

import base64
import hashlib
import io
import queue
import re
import threading
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import requests
from PIL import Image, ImageDraw, ImageTk
from playwright.sync_api import sync_playwright


MEDIA_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif", ".mp4", ".webm", ".mov", ".m4v"}
MAX_ITEMS = 150
MAX_PREVIEWS = 150


def valid_profile_url(value: str) -> bool:
    url = urlparse(value)
    host = (url.hostname or "").lower()
    return url.scheme == "https" and (host == "fatalmodel.com" or host.endswith(".fatalmodel.com"))


def file_extension(url: str, content_type: str = "") -> str:
    suffix = Path(unquote(urlparse(url).path)).suffix.lower()
    if suffix in MEDIA_EXTENSIONS:
        return suffix
    content_type = content_type.partition(";")[0].strip().lower()
    return {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp",
            "image/avif": ".avif", "image/gif": ".gif", "video/mp4": ".mp4",
            "video/webm": ".webm", "video/quicktime": ".mov",
            "video/x-m4v": ".mp4"}.get(content_type, "")


class BrowserWorker(threading.Thread):
    def __init__(self, inbox: queue.Queue, outbox: queue.Queue):
        super().__init__(daemon=True)
        self.inbox, self.outbox = inbox, outbox
        self.network_items: dict[str, dict] = {}

    @staticmethod
    def media_from_record(record: dict, base_url: str) -> dict | None:
        kind = str(record.get("type", "")).lower()
        if kind not in {"image", "photo", "video"}:
            return None
        media = record.get("media") or record.get("media_preview")
        if not isinstance(media, str) or not media:
            return None
        preview = record.get("thumbnail") or record.get("media_254x254") or media
        media_base = "https://files.fatalmodel.com" if media.startswith("/shared/") else base_url
        media_url = urljoin(media_base, media)
        preview_base = ("https://files.fatalmodel.com" if isinstance(preview, str) and
                        preview.startswith("/shared/") else base_url)
        preview_url = urljoin(preview_base, preview) if isinstance(preview, str) else ""
        if not media_url.startswith(("https://", "http://")):
            return None
        return {"id": str(record.get("post_id") or record.get("id") or media_url),
                "url": media_url, "kind": "vídeo" if kind == "video" else "foto",
                "previewUrl": preview_url, "width": 0, "height": 0,
                "videoIndex": -1, "preview": None}

    def capture_response(self, response) -> None:
        if "json" not in response.headers.get("content-type", "").lower():
            return
        host = (urlparse(response.url).hostname or "").lower()
        if host != "fatalmodel.com" and not host.endswith(".fatalmodel.com"):
            return
        try:
            stack = [response.json()]
            inspected = 0
            while stack and inspected < 10000:
                value = stack.pop()
                inspected += 1
                if isinstance(value, dict):
                    item = self.media_from_record(value, response.url)
                    if item:
                        self.network_items[item["id"]] = item
                    stack.extend(value.values())
                elif isinstance(value, list):
                    stack.extend(value)
        except Exception:
            pass

    def run(self) -> None:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            context = browser.new_context(accept_downloads=False)
            page = context.new_page()
            page.on("response", self.capture_response)
            while True:
                command, payload = self.inbox.get()
                try:
                    if command == "open":
                        self.network_items.clear()
                        page.goto(payload, wait_until="domcontentloaded", timeout=45000)
                        self.outbox.put(("status", "Perfil aberto. Clique em Carregar galeria para abrir todas as mídias."))
                    elif command == "scan":
                        self.outbox.put(("status", "Abrindo e percorrendo a galeria completa..."))
                        items, expected = self.scan(page)
                        self.outbox.put(("items", {"title": page.title(), "items": items,
                                                    "expected": expected}))
                    elif command == "download":
                        items, target = payload
                        self.download(context, page.url, items, Path(target))
                    elif command == "quit":
                        break
                except Exception as exc:
                    self.outbox.put(("error", str(exc)))
            browser.close()

    def scan(self, page) -> tuple[list[dict], int | None]:
        # O botão abre a galeria completa; a página do perfil mostra apenas uma prévia.
        expected = None
        open_button = page.locator('[data-testid="profile-gallery-view-all"]').first
        if not open_button.count():
            open_button = page.locator("button, a").filter(
                has_text=re.compile(r"Ver\s+\d+\s+m[ií]dias", re.IGNORECASE)
            ).first
        if open_button.count() and open_button.is_visible():
            label = open_button.inner_text()
            match = re.search(r"Ver\s+(\d+)\s+m[ií]dias", label, re.IGNORECASE)
            if match:
                expected = int(match.group(1))
            self.network_items.clear()
            gallery_href = open_button.get_attribute("href")
            if gallery_href:
                page.goto(urljoin(page.url, gallery_href), wait_until="domcontentloaded", timeout=45000)
            else:
                open_button.click()
            try:
                page.wait_for_url(re.compile(r"/galeria(?:[/?#]|$)"), timeout=15000)
            except Exception:
                pass
            page.wait_for_timeout(500)

        if expected is None and page.url.rstrip("/").endswith("/galeria"):
            total_tab = page.locator('[data-testid="gallery-tab-all-page"]').first
            if total_tab.count():
                match = re.search(r"\d+", total_tab.inner_text())
                if match:
                    expected = int(match.group())

        found = {}
        stable_rounds = 0
        previous_count = -1
        for _ in range(30):
            raw = page.evaluate("""() => {
          const normalize = s => (s || '').normalize('NFD').replace(/[\\u0300-\\u036f]/g, '').toLowerCase();
          const visible = el => !!(el && el.getClientRects().length);
          const modal = [...document.querySelectorAll('[role="dialog"], dialog, [aria-modal="true"]')]
            .filter(visible).at(-1);
          const headings = [...document.querySelectorAll('h1,h2,h3,h4,[role="heading"]')];
          const heading = headings.find(el => /galeria|fotos|midias/.test(normalize(el.innerText)));
          let section = location.pathname.endsWith('/galeria') ?
            (document.querySelector('[data-testid="gallery-page"]') || document.body) :
            (modal || (heading && (heading.closest('section, article, [role="region"]') || heading.parentElement)));
          for (let i = 0; i < 5 && section && !section.querySelector('img,video'); i++)
            section = section.parentElement;
          if (!section) return {error: 'Não encontrei a galeria aberta. Clique em “Ver mídias” e tente novamente.'};
          const items = [];
          const add = (url, kind, previewUrl='', width=0, height=0, videoIndex=-1, id='') => {
            if ((url && /^https?:/i.test(url)) || (kind === 'vídeo' && id))
              items.push({url, kind, previewUrl, width, height, videoIndex, id});
          };
          const videoPattern = /\\.(mp4|webm|mov|m4v)(?:[?#]|$)/i;
          const imagePattern = /\\.(jpe?g|png|webp|gif|avif)(?:[?#]|$)/i;
          for (const image of section.querySelectorAll('img')) {
            const source = image.currentSrc || image.src;
            const link = image.closest('a[href]');
            const card = image.closest('.grid-gallery__post');
            if (card && card.querySelector('.grid-gallery__post-video'))
              add(link && videoPattern.test(link.href) ? link.href : '', 'vídeo', source,
                  image.naturalWidth, image.naturalHeight, -1, image.id);
            else if (link && videoPattern.test(link.href))
              add(link.href, 'vídeo', source, 0, 0, -1, image.id);
            else if (!image.closest('video'))
              add(image.getAttribute('data-full') || image.getAttribute('data-original') ||
                  (link && imagePattern.test(link.href) ? link.href : source),
                  'foto', source, image.naturalWidth, image.naturalHeight, -1, image.id);
          }
          const allVideos = [...document.querySelectorAll('video')];
          for (const video of section.querySelectorAll('video')) {
            add(video.currentSrc || video.src || video.querySelector('source')?.src,
                'vídeo', video.poster || '', 0, 0, allVideos.indexOf(video));
          }
          for (const link of section.querySelectorAll('a[href]')) {
            if (videoPattern.test(link.href)) {
              const image = link.querySelector('img');
              add(link.href, 'vídeo', image ? (image.currentSrc || image.src) : '');
            }
          }
          const metadata = [];
          const payload = document.querySelector('#__NUXT_DATA__');
          if (payload) {
            try {
              const values = JSON.parse(payload.textContent);
              for (const entry of values) {
                if (!entry || typeof entry !== 'object' || Array.isArray(entry) ||
                    !('post_id' in entry) || !('media' in entry) || !('type' in entry)) continue;
                metadata.push({post_id: values[entry.post_id], type: values[entry.type],
                  media: values[entry.media], media_preview: values[entry.media_preview],
                  thumbnail: values[entry.thumbnail]});
              }
            } catch (_) {}
          }
          return {items, metadata};
            }""")
            if raw.get("error"):
                raise RuntimeError(raw["error"])
            metadata = [self.media_from_record(record, page.url)
                        for record in raw.get("metadata", [])]
            for item in [*raw["items"], *[x for x in metadata if x],
                         *list(self.network_items.values())]:
                url = item.get("url") or ""
                key = str(item.get("id") or url)
                if not key or (not url and item.get("kind") != "vídeo"):
                    continue
                if url and not url.startswith(("https://", "http://")):
                    continue
                if item["kind"] == "foto" and item.get("width") and item.get("height"):
                    if item["width"] < 120 or item["height"] < 120:
                        continue
                if key not in found and len(found) >= MAX_ITEMS:
                    continue
                previous = found.get(key, {})
                if not url and previous.get("url"):
                    continue
                found[key] = {**previous, **item,
                              "previewUrl": item.get("previewUrl") or previous.get("previewUrl") or "",
                              "preview": previous.get("preview")}
            if expected and len(found) >= expected:
                break
            stable_rounds = stable_rounds + 1 if len(found) == previous_count else 0
            previous_count = len(found)
            moved = page.evaluate("""() => {
              const visible = el => !!(el && el.getClientRects().length);
              const modal = [...document.querySelectorAll('[role="dialog"], dialog, [aria-modal="true"]')]
                .filter(visible).at(-1);
              const root = modal || document.body;
              const scrollables = [...root.querySelectorAll('*')].filter(el => {
                const style = getComputedStyle(el);
                return el.scrollHeight > el.clientHeight + 50 && el.clientHeight > 120 &&
                  /auto|scroll/.test(style.overflowY);
              });
              const target = scrollables.sort((a, b) => b.clientHeight - a.clientHeight)[0] ||
                document.scrollingElement;
              const before = target.scrollTop;
              target.scrollTop = Math.min(target.scrollHeight,
                before + Math.max(500, target.clientHeight * 0.85));
              return target.scrollTop > before;
            }""")
            if page.url.rstrip("/").endswith("/galeria"):
                more = page.locator("button, a").filter(
                    has_text=re.compile(r"^(carregar|mostrar|ver)\s+mais", re.IGNORECASE)
                ).first
                if more.count() and more.is_visible():
                    more.click()
                    moved = True
            page.wait_for_timeout(350)
            if stable_rounds >= 3 and not moved:
                break

        session = self.make_session(page.context, page.url)
        for index, item in enumerate(list(found.values())[:MAX_PREVIEWS], 1):
            if index == 1 or index % 10 == 0:
                self.outbox.put(("status", f"Preparando miniaturas: {index}/{len(found)}..."))
            preview_url = item.get("previewUrl") or ""
            try:
                if not preview_url.startswith(("https://", "http://")):
                    raise ValueError("sem imagem de capa")
                with session.get(preview_url, timeout=15, stream=True) as response:
                    response.raise_for_status()
                    if not response.headers.get("Content-Type", "").lower().startswith("image/"):
                        continue
                    data = response.raw.read(3 * 1024 * 1024 + 1)
                    if len(data) > 3 * 1024 * 1024:
                        continue
                with Image.open(io.BytesIO(data)) as image:
                    image = image.convert("RGB")
                    image.thumbnail((176, 132))
                    buffer = io.BytesIO()
                    image.save(buffer, format="PNG", optimize=True)
                    item["preview"] = buffer.getvalue()
            except Exception:
                if item["kind"] == "vídeo" and item.get("videoIndex", -1) >= 0:
                    try:
                        item["preview"] = page.locator("video").nth(item["videoIndex"]).screenshot(timeout=2500)
                    except Exception:
                        pass
        return list(found.values()), expected

    @staticmethod
    def make_session(context, referer: str) -> requests.Session:
        session = requests.Session()
        session.headers.update({"User-Agent": "Mozilla/5.0", "Referer": referer})
        for cookie in context.cookies():
            session.cookies.set(cookie["name"], cookie["value"], domain=cookie["domain"], path=cookie["path"])
        return session

    def download(self, context, referer: str, items: list[dict], target: Path) -> None:
        target.mkdir(parents=True, exist_ok=True)
        session = self.make_session(context, referer)
        ok, failed = 0, []
        for number, item in enumerate(items, 1):
            try:
                if item["kind"] == "vídeo":
                    extension = file_extension(item["url"]) or ".mp4"
                    digest = hashlib.sha256(item["url"].encode("utf-8")).hexdigest()[:12]
                    destination = target / f"vídeo_{digest}{extension}"
                    self.download_browser_video(context, item["url"], destination)
                    ok += 1
                    self.outbox.put(("progress", (number, len(items))))
                    continue
                with session.get(item["url"], stream=True, timeout=45) as response:
                    response.raise_for_status()
                    content_type = response.headers.get("Content-Type", "")
                    ext = file_extension(item["url"], content_type)
                    if not ext or not (content_type.startswith("image/") or content_type.startswith("video/")):
                        raise ValueError("link não entrega uma foto ou vídeo direto")
                    digest = hashlib.sha256(item["url"].encode("utf-8")).hexdigest()[:12]
                    destination = target / f"{item['kind']}_{digest}{ext}"
                    with destination.open("wb") as output:
                        for chunk in response.iter_content(256 * 1024):
                            if chunk:
                                output.write(chunk)
                ok += 1
            except Exception as exc:
                failed.append(f"{number}: {exc}")
            self.outbox.put(("progress", (number, len(items))))
        self.outbox.put(("done", (ok, failed, str(target))))

    @staticmethod
    def download_browser_video(context, url: str, destination: Path) -> None:
        media_page = context.new_page()
        media_page.set_default_timeout(180000)
        temporary = destination.with_suffix(destination.suffix + ".part")
        try:
            response = media_page.goto(url, wait_until="commit", timeout=45000)
            if response is None or response.status >= 400:
                status = response.status if response else "sem resposta"
                raise RuntimeError(f"o navegador não conseguiu abrir o vídeo (HTTP {status})")

            bytes_written = 0
            with temporary.open("wb") as output:
                def append_chunk(encoded: str) -> None:
                    nonlocal bytes_written
                    data = base64.b64decode(encoded)
                    output.write(data)
                    bytes_written += len(data)

                media_page.expose_function("appendMediaChunk", append_chunk)
                result = media_page.evaluate("""async url => {
                  const response = await fetch(url, {
                    credentials: 'include', headers: {Range: 'bytes=0-'}
                  });
                  if (!response.ok || !response.body)
                    return {status: response.status, error: 'arquivo indisponível'};
                  const reader = response.body.getReader();
                  while (true) {
                    const {done, value} = await reader.read();
                    if (done) break;
                    for (let start = 0; start < value.length; start += 32768) {
                      const slice = value.subarray(start, start + 32768);
                      await window.appendMediaChunk(btoa(String.fromCharCode(...slice)));
                    }
                  }
                  return {status: response.status,
                    length: response.headers.get('content-length'),
                    range: response.headers.get('content-range'),
                    type: response.headers.get('content-type')};
                }""", url)
                output.flush()

            if result.get("error") or not result.get("type", "").lower().startswith("video/"):
                raise RuntimeError(f"o navegador não recebeu um arquivo de vídeo (HTTP {result.get('status')})")
            if bytes_written == 0:
                raise RuntimeError("o vídeo chegou vazio")
            content_range = result.get("range") or ""
            match = re.match(r"bytes\s+(\d+)-(\d+)/(\d+)", content_range)
            if match and (int(match.group(1)) != 0 or bytes_written != int(match.group(3))):
                raise RuntimeError("o vídeo foi recebido apenas parcialmente")
            if not match and result.get("length") and bytes_written != int(result["length"]):
                raise RuntimeError("o tamanho recebido não corresponde ao arquivo")
            temporary.replace(destination)
        finally:
            media_page.close()
            if temporary.exists():
                temporary.unlink()


class App:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Galeria de mídias | Fatal Model")
        self.root.geometry("1040x720")
        self.root.minsize(840, 580)
        self.root.configure(bg="#f3f6fa")
        self.inbox, self.outbox = queue.Queue(), queue.Queue()
        self.worker = BrowserWorker(self.inbox, self.outbox)
        self.worker.start()
        self.items: list[dict] = []
        self.thumb_images = []
        self.card_columns = 0
        self.url = tk.StringVar()
        self.folder = tk.StringVar(value=str(Path.home() / "Downloads" / "midias_perfil"))
        self.status = tk.StringVar(value="Cole o link de um perfil Fatal Model.")
        self.build()
        self.root.after(100, self.poll)
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def build(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#f3f6fa")
        style.configure("TLabel", background="#f3f6fa", foreground="#263449", font=("Segoe UI", 10))
        style.configure("Title.TLabel", font=("Segoe UI", 19, "bold"), foreground="#14243a")
        style.configure("Sub.TLabel", foreground="#607087")
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=(12, 8),
                        background="#e2eaf3", foreground="#23354d", borderwidth=0)
        style.map("TButton", background=[("active", "#d3dfec")])
        style.configure("Accent.TButton", background="#087f8c", foreground="white")
        style.map("Accent.TButton", background=[("active", "#066b76")])
        style.configure("Treeview", rowheight=82, font=("Segoe UI", 10), background="white",
                        fieldbackground="white", foreground="#263449", borderwidth=0)
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"), background="#e7edf4",
                        foreground="#4b5d73", padding=9, relief="flat")
        style.map("Treeview", background=[("selected", "#d6f0f0")], foreground=[("selected", "#14243a")])

        outer = ttk.Frame(self.root, padding=20)
        outer.pack(fill="both", expand=True)
        ttk.Label(outer, text="Galeria de mídias", style="Title.TLabel").pack(anchor="w")
        ttk.Label(outer, text="Fotos e vídeos em uma grade, com botão de download em cada item.",
                  style="Sub.TLabel").pack(anchor="w", pady=(2, 16))

        linkbox = ttk.Frame(outer, padding=14)
        linkbox.pack(fill="x", pady=(0, 12))
        ttk.Label(linkbox, text="LINK DO PERFIL", font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(0, 7))
        row = ttk.Frame(linkbox)
        row.pack(fill="x")
        ttk.Entry(row, textvariable=self.url, font=("Segoe UI", 10)).pack(side="left", fill="x", expand=True, ipady=6)
        ttk.Button(row, text="Abrir perfil", command=self.open).pack(side="left", padx=(8, 0))
        ttk.Button(row, text="Carregar galeria", style="Accent.TButton", command=self.scan).pack(side="left", padx=(8, 0))
        ttk.Label(outer, text="O app abre o link “Ver mídias” e percorre a galeria automaticamente.",
                  style="Sub.TLabel").pack(anchor="w", pady=(0, 8))

        gallery = ttk.Frame(outer)
        gallery.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(gallery, background="#f3f6fa", borderwidth=0, highlightthickness=0)
        scroll = ttk.Scrollbar(gallery, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scroll.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        self.card_host = ttk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.card_host, anchor="nw")
        self.card_host.bind("<Configure>", lambda event: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", self.on_canvas_resize)
        self.canvas.bind_all("<MouseWheel>", lambda event: self.canvas.yview_scroll(int(-event.delta / 120), "units"))

        bottom = ttk.Frame(outer, padding=(0, 12, 0, 0))
        bottom.pack(fill="x")
        ttk.Button(bottom, text="Pasta de destino", command=self.choose_folder).pack(side="left")
        ttk.Entry(bottom, textvariable=self.folder).pack(side="left", fill="x", expand=True, ipady=5)
        ttk.Button(bottom, text="Baixar tudo", style="Accent.TButton", command=self.download_all).pack(side="left", padx=(8, 0))
        ttk.Label(outer, textvariable=self.status, wraplength=980).pack(anchor="w", pady=(12, 0))

    def open(self) -> None:
        value = self.url.get().strip()
        if not valid_profile_url(value):
            messagebox.showerror("Link inválido", "Cole uma URL HTTPS do domínio fatalmodel.com.")
            return
        self.status.set("Abrindo navegador...")
        self.inbox.put(("open", value))

    def scan(self) -> None:
        self.inbox.put(("scan", None))

    def choose_folder(self) -> None:
        chosen = filedialog.askdirectory(initialdir=self.folder.get())
        if chosen:
            self.folder.set(chosen)

    def download_one(self, item: dict) -> None:
        if not item.get("url"):
            messagebox.showinfo("Vídeo indisponível", "A galeria mostrou a capa, mas não forneceu um arquivo de vídeo direto.")
            return
        destination = Path(self.folder.get()).expanduser()
        self.status.set("Baixando 1 arquivo...")
        self.inbox.put(("download", ([item], str(destination))))

    def download_all(self) -> None:
        if not self.items:
            messagebox.showinfo("Galeria vazia", "Carregue a galeria primeiro.")
            return
        available = [item for item in self.items if item.get("url")]
        if not available:
            messagebox.showinfo("Sem arquivos diretos", "A galeria ainda não forneceu arquivos para baixar.")
            return
        destination = Path(self.folder.get()).expanduser()
        self.status.set(f"Baixando {len(available)} arquivo(s)...")
        self.inbox.put(("download", (available, str(destination))))

    def on_canvas_resize(self, event) -> None:
        self.canvas.itemconfigure(self.canvas_window, width=event.width)
        columns = max(2, min(4, event.width // 245))
        if columns != self.card_columns:
            self.card_columns = columns
            self.render_cards()

    def render_cards(self) -> None:
        for child in self.card_host.winfo_children():
            child.destroy()
        self.thumb_images.clear()
        columns = max(1, self.card_columns)
        for column in range(columns):
            self.card_host.grid_columnconfigure(column, weight=1)
        for index, item in enumerate(self.items):
            card = tk.Frame(self.card_host, bg="white", highlightbackground="#dce5ef",
                            highlightthickness=1, padx=9, pady=9)
            card.grid(row=index // columns, column=index % columns,
                      padx=8, pady=8, sticky="n")
            picture = Image.new("RGB", (210, 150), "#dce5ef")
            if item.get("preview"):
                try:
                    with Image.open(io.BytesIO(item["preview"])) as source:
                        source = source.convert("RGB")
                        source.thumbnail((210, 150))
                        picture.paste(source, ((210 - source.width) // 2, (150 - source.height) // 2))
                except Exception:
                    pass
            if item["kind"] == "vídeo":
                draw = ImageDraw.Draw(picture)
                draw.ellipse((80, 50, 130, 100), fill="#087f8c")
                draw.polygon([(98, 64), (98, 86), (117, 75)], fill="white")
            photo = ImageTk.PhotoImage(picture)
            self.thumb_images.append(photo)
            tk.Label(card, image=photo, bg="white").pack()
            tk.Label(card, text=item["kind"].upper(), bg="white", fg="#607087",
                     font=("Segoe UI", 9, "bold")).pack(pady=(7, 4))
            button = ttk.Button(card, text="Baixar" if item.get("url") else "Sem arquivo direto",
                                style="Accent.TButton",
                                command=lambda current=item: self.download_one(current))
            if not item.get("url"):
                button.state(["disabled"])
            button.pack(fill="x")

    def poll(self) -> None:
        try:
            while True:
                kind, value = self.outbox.get_nowait()
                if kind == "status":
                    self.status.set(value)
                elif kind == "items":
                    self.items = value["items"]
                    self.render_cards()
                    photos = sum(item["kind"] == "foto" for item in self.items)
                    videos = sum(item["kind"] == "vídeo" for item in self.items)
                    expected = value.get("expected")
                    count = f" de {expected} anunciadas" if expected else ""
                    self.status.set(f"{photos} foto(s) e {videos} vídeo(s) encontrados{count} na galeria.")
                elif kind == "progress":
                    self.status.set(f"Baixando {value[0]}/{value[1]}...")
                elif kind == "done":
                    ok, failed, folder = value
                    self.status.set(f"{ok} arquivo(s) salvos em {folder}; {len(failed)} falha(s).")
                    if failed:
                        messagebox.showwarning("Alguns arquivos falharam", "\n".join(failed[:10]))
                elif kind == "error":
                    self.status.set("Erro: " + value)
        except queue.Empty:
            pass
        self.root.after(100, self.poll)

    def close(self) -> None:
        self.inbox.put(("quit", None))
        self.root.destroy()

    def run(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    App().run()
