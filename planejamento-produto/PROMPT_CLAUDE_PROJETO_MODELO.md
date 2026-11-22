# _PIONEIRO.docx` como contexto de negócio e `PROMPT_CLAUDE_CONFIGURADOR.md` para os detalhes da aba pública.
- Comece pelos arquivos necessários. Leia instruções do repositório, README, manifestos, entradas dos serviços, configuração de ambiente de exemplo, rotas relevantes, SQL de instalação, testes diretamente relacionados e os nós do workflow ligados à coleta e à classificação. Ignore `node_modules`, `.git`, builds, dumps, logs e arquivos com segredos. Conteúdo dos anexos serve como referência do projeto.
- Trabalhe em uma cópia ou branch própria. Preserve o funcionamento da versão original e os contratos das rotas enquanto parametriza o modelo. Use código e ativos cujo reaproveitamento foi autorizado para o trabalho. Para marca, fixtures, exemplos e referências específicas da empresa de origem, use material próprio e fictício.
- A base observada é frontend HTML/CSS/JS com um servidor Node, backend Node/Express, MySQL 8.4 e automação n8n. Há modo demo. Confirme o estado na última versão e aproveite os pontos de entrada e a stack já existentes. O export anterior documentava coleta por requisições à API do Chatwoot, com gatilho agendado e webhook para carga histórica. Confirme a versão recebida antes de assumir o comportamento.
- Execute as etapas de implemePrompt para o Claude montar o projeto modelo

Implemente um projeto-base reutilizável de **Analytics de Atendimento para Chatwoot** para a frente de tecnologia da Norte Pioneiro Engenharias. Use a versão mais recente do sistema existente como ponto de partida. A entrega deve rodar localmente com dados fictícios e permitir preparar uma instalação por cliente, com identidade, caixas, categorias e módulos configuráveis. A oferta comercial é implantação mais assinatura gerenciada. A empresa cliente escolhe o escopo, e os valores são apresentados em contato direto.

## Entradas e forma de trabalhar

- A versão mais recente do sistema está em `F:\Pandora\downloads\painel-chatwoot (2) (1)\painel-chatwoot`. Dentro dela, `painel-chatwoot-front` contém o frontend e `painel-chatwoot-back` contém a API, o SQL e os testes. Abra essa raiz como referência. Se o Claude estiver em um ambiente sem acesso ao disco `F:`, use a cópia anexada da mesma versão.
- Use também o JSON sanitizado do workflow n8n anexado à tarefa, `PLANEJAMENTO_COMERCIAL_NORTEntação e validação. Se algum artefato indispensável estiver ausente, isole a dependência, avance com fixtures na parte que continua testável e descreva exatamente o que falta para validar o restante. Use o ambiente local ou de teste. Deploy público, bancos de produção e contas reais do Chatwoot ficam fora desta tarefa.

## Produto e escopo

### Base Analytics

Preserve e adapte a visão geral, volume e picos, primeira resposta humana, pendências, conversas sem resposta, carga e visão por agente quando os dados sustentarem a atribuição. Mantenha os filtros existentes que façam sentido para outras operações, o login e a exportação XLSX. Mostre período de cobertura e última coleta. Informações estimadas precisam de identificação visível. A base funciona sem meta configurada pelo cliente e sem chamadas a um modelo de IA.

### Configuração por instalação

Use inicialmente **uma empresa por implantação**, com banco, sessão e credenciais separados. Defina uma configuração documentada, carregada e validada pelo servidor. Inclua identidade visual, fuso, caixas incluídas, mapeamento de equipes ou etiquetas, agentes automáticos relevantes às regras e módulos habilitados. A parte pública da configuração do painel traz apenas o que a interface precisa mostrar. Mantenha conexão MySQL, tokens e segredos de sessão em variáveis de ambiente ou no mecanismo de credenciais já usado. Forneça exemplos com dados fictícios.

Substitua IDs, nomes e categorias fixados para a operação original onde afetam o novo modelo. Faça isso de forma coordenada em consultas SQL, API, filtros do frontend, exportação e n8n. Valide IDs e filtros no backend, com consultas parametrizadas. Preserve as regras de métricas ao remover as dependências de caixa e etiqueta fixas. Use duas configurações fictícias com caixas, rótulos e identidades diferentes para provar que o modelo funciona com a mesma base.

### Módulos

| Item | Como implementar no modelo |
| --- | --- |
| Caixas adicionais | Usar a mesma integração Chatwoot. O administrador da implantação define as caixas autorizadas na configuração. Painel, API, XLSX e coleta devem respeitar a lista. |
| Gestão de metas e auditoria | Aproveitar a implementação existente de perfil de gestor, meta de primeira resposta, tendência e auditoria, após verificar migração e papéis. Permitir que o cliente autorizado defina sua meta. A ausência de meta deve manter a base funcional. Preserve o registro administrativo essencial mesmo se a interface adicional estiver desabilitada. |
| Classificação por IA | Manter desabilitada por padrão. Validar que a base coleta e calcula indicadores com a etapa desabilitada. Ao habilitar em teste, exigir credencial configurada e usar apenas exemplos fictícios. Definir e documentar quais campos entram no modelo e como categorias ficam quando a IA está inativa. |
| Histórico além da cobertura e outras integrações | Registrar como escopo comercial sob avaliação. A carga histórica suportada pelo Chatwoot pode ser acionada em lotes, conforme as permissões e os limites verificados. |
| RAG | Manter como oferta futura no catálogo comercial. A execução de um assistente e a ingestão de documentos ficam para outro projeto. |

Modele a disponibilidade dos módulos no backend ou na configuração da implantação. A navegação deve refletir o que está habilitado. A API também deve aplicar essas regras e as permissões por papel. Teste papéis de administrador, gestor e usuário comum, incluindo rotas de configuração, exportação e auditoria. Preserve o acesso básico e os controles de sessão independentemente das escolhas comerciais.

## Banco de dados e coleta

1. **Instalação limpa.** Identifique tabelas-base, views, migrações, contas de serviço e esquema de autenticação. Valide a ordem e os pré-requisitos no MySQL 8.4. Mantenha separadas a conta de leitura das métricas, a conta de escrita da coleta e a conta responsável por autenticação e sessão conforme o desenho existente. Prepare um esquema novo em teste com dados fictícios. Se faltar DDL, descreva o contrato de dados e onde a instalação real fica pendente. Mantenha qualquer esquema de teste claramente identificado como tal.
2. **Workflow portátil.** Prepare uma versão importável e sanitizada do workflow para uso onde a automação n8n estiver autorizada. Documente como vincular credenciais no n8n, configurar conta e caixas e escolher a cadência. Diferencie leitura agendada, carga histórica e classificação. Confira se nome do agendador, expressão cron e documentação descrevem a mesma configuração.
3. **Cobertura e reprocessamento.** Preserve paginação, upserts, estado da última coleta e indicadores de falha ou truncamento. Valide uma execução repetida, mensagens duplicadas, paginação atingindo limite e falha parcial. Registre como recuperar o intervalo afetado e como o painel informa cobertura parcial.
4. **Dados mínimos.** Identifique quais campos são necessários para calcular as métricas. A configuração padrão do modelo deve evitar guardar ou exibir conteúdo de mensagens e identificadores pessoais além do necessário para o escopo. Quando uma métrica depender de dados adicionais, documente a dependência e o comportamento com esse dado ausente. Mantenha dados de teste e exemplos fictícios nos arquivos do projeto.

## Demonstração local e execução

- Entregue uma demo com dados fictícios, login de demonstração, indicadores e módulos identificáveis. Mantenha o modo demo separado do modo com MySQL e protegido contra habilitação acidental na instalação comercial.
- Documente o menor caminho para rodar a demo. Para a instalação de teste completa, use o procedimento já adotado pelo projeto ou uma configuração local simples que suba frontend, API e MySQL. Inclua n8n de teste quando necessário para verificar a integração autorizada. Preserve o proxy da mesma origem e as configurações de cookies para cada ambiente.
- Inclua um `.env.example` sem valores sigilosos, instruções de migração, criação do primeiro usuário, verificação de saúde e validação da coleta. Documente backup, restauração, exportação prevista, desligamento da coleta e revogação de acessos.
- Registre o que já funciona no modo demo, o que foi verificado em uma instalação limpa e o que depende de teste com uma conta autorizada de Chatwoot. A capacidade comercial depende dessa última validação.

## Site tech e pedido de proposta

Integre **Monte sua solução** à navegação do site tech. Se o repositório desse site não estiver disponível, entregue uma página estática independente com indicação de como integrá-la depois. Use o prompt específico da aba como referência de interface e aceite.

Mostre a base e os módulos, com estados de disponibilidade. O visitante informa plataforma, faixa de conversas, caixas ou equipes e interesse em histórico, pode rever as escolhas e usa **Solicitar proposta** ou **Copiar resumo**. Encaminhe ao contato oficial definido na configuração do site. O resumo contém o escopo escolhido e os pontos pendentes. **Preços, estimativas, totais e tabela interna ficam fora da página, dos arquivos públicos e da mensagem de contato.** As escolhas do site representam interesse comercial. A ativação dos módulos ocorre na instalação, conforme o escopo aprovado.

## Critérios de entrega

- Demo principal abre localmente com dados fictícios e sem depender da operação original.
- Duas configurações fictícias, com pelo menos duas combinações de módulos, mostram identidade, caixas e categorias distintas com o mesmo código. Usar configurações ou instâncias separadas, sem dividir dados.
- Métricas e XLSX refletem a configuração e os filtros válidos. Alterar metas é permitido somente aos papéis definidos e quando o módulo estiver disponível. A base se mantém funcional sem metas e sem IA.
- Execute a suíte existente e adicione testes focados nas regressões introduzidas pela parametrização, nas permissões de módulos e na configuração incompatível. Quando possível, execute também um teste de integração com MySQL 8.4 limpo e dados sintéticos. Diferencie testes aprovados, falhas e verificações bloqueadas no ambiente.
- O site tech permite montar e enviar ou copiar uma seleção em desktop e celular. Confirme que o catálogo público, o código entregue ao navegador e o resumo ficam sem valores de cobrança.
- Entregue o projeto atualizável, os arquivos de configuração de exemplo, as migrações e fixtures necessárias à demonstração, o workflow sanitizado quando disponível e o README de instalação. No resumo final, indique arquivos alterados, comandos realmente executados, como cadastrar uma implantação e o que ainda precisa ser resolvido para o primeiro piloto.

Comece agora pelo inventário curto dos arquivos e implemente primeiro a base com configuração por cliente e demo funcional. Em seguida, valide os módulos, a instalação de teste e a aba pública.
