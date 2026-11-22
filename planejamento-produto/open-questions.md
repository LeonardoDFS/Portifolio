# Perguntas em aberto e evidências necessárias

**Escopo atual.** Planejar a comercialização do sistema existente. Priorizar titularidade e licenças, modelo de assinatura, regras de cobrança, contratos, responsabilidades, suporte e regras de entrada e saída. O código, o SQL e o JSON do n8n recebidos em 16/11/2026 já sustentam um inventário parcial. [Diagnóstico](product-1-roadmap.md#diagnóstico-do-material-recebido-em-16112026)

| Prioridade | Pergunta | Como confirmar | Decisão dependente |
| --- | --- | --- | --- |
| Antes de ofertar o sistema existente | Quem detém os direitos sobre código, fluxos, exemplos, arquitetura proprietária, infraestrutura e dados da solução original? Quais contratos, políticas e licenças incidem? | Revisar atribuições, registros do projeto, políticas, licenças e eventual autorização escrita do titular. Consultar assessoria jurídica com os fatos caso haja interesse em reaproveitar o backend. | Decidir sob quais condições o sistema existente pode integrar a oferta. [Registro do tópico 1](#1-titularidade-da-solução-original) |
| Protótipo e validação comercial | Que informação operacional demonstrar e qual lacuna valeria pagar para resolver? | Demonstrar com dados sintéticos. Comparar com os relatórios nativos do Chatwoot e validar a utilidade com prospects. | Medir tempo de primeira resposta humana, volume por horário e casos pendentes. O cliente define o uso dos indicadores e eventuais metas de equipe. [Registro do tópico 2](#2-problema-e-funções-do-protótipo) |
| Antes de definir o escopo da implantação | Que permissões e tarefas a integração exige no cliente? | Validar o workflow e as credenciais de leitura em uma conta de teste autorizada. Documentar quem configura o acesso e dispara a carga histórica. | A coleta exportada consulta a API do Chatwoot. O webhook é um gatilho da carga. [Registro do tópico 3](#3-fonte-do-primeiro-conector) |
| Antes de comprometer cobertura | Que alcance há para histórico, estados, transições, ator humano, fila, mensagens automáticas, transferências e horários? | Conferir documentação e evidência autorizada da solução existente. | Definir os limites que podem constar na proposta. [Registro do tópico 4](#4-cobertura-dos-eventos-e-histórico) |
| Antes do piloto | Qual finalidade, base legal, retenção, papel de tratamento, política de funcionários e fluxo de destruição? Existem dados sensíveis ou de menores? | Cliente e fornecedor mapeiam campos, usos, subprocessadores, transferências e fluxo de acesso. Validar contrato e segurança. | Campos que podem ser coletados, acessados e armazenados. |
| Antes de contratar n8n | A topologia, as credenciais e o uso do n8n estão cobertos por licença vigente? | Descrever hospedagem, acesso e valor comercial ao fornecedor e registrar resposta escrita. | n8n licenciado, consultoria no ambiente do cliente ou worker próprio. |
| Antes da instalação de teste | Qual esquema cria as tabelas-base e quais versões, permissões e recursos de infraestrutura são necessários? | Complementar inventário Node/Express, MySQL e n8n com DDL das tabelas-base, procedimento de setup e parâmetros de uma configuração de teste. | Reproduzir implantação em ambiente próprio autorizado. |
| Antes de prometer cadência e histórico | Qual configuração está publicada? Como retomar após falhas, atingir cobertura e conciliar etiquetas? | Comparar agendamento exportado, logs e cobertura de uma execução autorizada. A coleta agendada revisita uma janela de atividade e tem limites de paginação. | Fixar cadência, limites e recuperação na proposta. |
| Antes de prometer suporte e capacidade | Quais volumes e custos foram medidos? Como funciona recuperação? Qual isolamento é necessário por cliente? | Rodar testes HTTP em ambiente que aceite loopback, verificar o setup com MySQL, ensaiar backup e restauração e medir um cenário representativo. | Dimensionar hospedagem, suporte e dados de saída. |
| Antes da assinatura recorrente | Horas de setup/suporte e custos são compatíveis com os três planos? Quem compra e quanto tempo leva? | Medir piloto, custos, objeções e escolha entre opções com preço. | Franquia, margem, suporte e cadência comercial. |
| Antes de centralizar | Dois clientes repetiram o mesmo conector? Quais perfis, volumes, exigências de dedicação e RPO/RTO surgiram? | Medir as instalações, validar recuperação e testar autorização por empresa. | SaaS, dedicação ou híbrido. |
| Antes de propor RAG | Qual tarefa merece investimento, qual corpus é autorizado, quem atualiza e quais erros são inaceitáveis? | Entrevista, amostra, conjunto de avaliação e revisão contratual e de privacidade. | Modelo, armazenamento, integração e supervisão. |

**Estado das evidências.** A revisão local não confirma o estado da implantação original. O arquivo de configuração com valores reais ou potenciais segredos ficou fora da leitura. Para material comercial, usar conteúdo e dados fictícios próprios, com origem documentada e direitos verificados.

## 1. Titularidade da solução original

**Relato do proponente.** A solução surgiu durante a relação de emprego para atender a uma necessidade da empresa. A coleta, o backend e o frontend foram construídos no projeto. O n8n roda em uma VPS e a empresa fornece servidores para os dados e o acesso à aplicação. O proponente relata ter concebido a lógica da API, com auxílio de sua conta pessoal do Claude, e ter interesse em reaproveitar o backend. Relata ainda não ter assinado contrato de trabalho escrito e desconhece cláusula específica sobre o software. Os detalhes técnicos aguardam confirmação.

**Decisão de planejamento.** Estruturar a proposta comercial considerando o sistema funcional relatado. A inclusão da API original e de demais componentes na oferta fica condicionada à verificação da titularidade e à autorização escrita do titular para o uso comercial dos componentes identificados. A escolha de uma solução técnica futura fica pendente caso o uso do sistema existente não seja viável.

**Evidência pendente.** O art. 4º da Lei do Software considera a relação do desenvolvimento com as atividades do vínculo e as estipulações existentes. A CLT prevê contrato tácito, verbal ou escrito. O relato dá motivo para verificar as atribuições e as políticas internas antes de assumir direito de exploração do código. A titularidade definitiva permanece em aberto. [Lei do Software, art. 4º](https://sisatos.datalegis.net/action/ActionDatalegis.php?acao=abrirTextoAto&cod_menu=10423&cod_modulo=680&link=S&numeroAto=00009609&orgao=000&seq_ato=000&tipo=LEI&valorAno=1998) · [CLT, arts. 442 e 443](https://www2.camara.leg.br/legin/fed/declei/1940-1949/decreto-lei-5452-1-maio-1943-415500-normaatualizada-pe.html)

## 2. Problema e funções do protótipo

**Relato do proponente.** A ideia surgiu ligada à automação do chat de atendimento. A operação queria enxergar horários de pico, demora no retorno e desempenho por atendente. A responsabilidade pelo acompanhamento seria do gestor da área, com quem o proponente ainda não tem contato. O proponente acredita que a operação ainda não tem meta definida e vê o painel como instrumento de acompanhamento e engajamento. A fonte informada é o Chatwoot.

**Decisão de planejamento.** O protótipo comercial demonstra volume por faixa horária, tempo até a primeira resposta humana, conversas aguardando retorno e visão por agente quando a atribuição for verificável. Esses indicadores funcionam sem configuração de meta. Cada cliente decide como os usa e se deseja configurar metas. Comparar a demonstração com os relatórios nativos do Chatwoot para verificar se o painel ou os alertas resolvem uma lacuna pela qual um prospect pagaria.

**Atribuição no Chatwoot.** O remetente da mensagem ajuda a identificar quem respondeu. Para associar uma espera a alguém, verificar se havia um responsável atribuído no intervalo analisado e se houve transferências. Se isso não puder ser reconstituído, manter a pendência na visão da fila. A documentação mostra objetos e eventos pertinentes, e a cobertura da instalação permanece em aberto. [Webhooks do Chatwoot](https://www.chatwoot.com/hc/user-guide/articles/1777049924-como-usar-webhooks)

**A confirmar comercialmente.** Quais lacunas os prospects percebem na ferramenta atual e quais funções valorizam o suficiente para contratar. A rotina e as metas do setor que inspirou o projeto ficam a cargo da operação.

## 3. Fonte do primeiro conector

**Relato do proponente.** A empresa administra agentes e regras em uma conta administrativa do Chatwoot. Na solução original, o n8n recebe eventos para leitura via webhooks do Chatwoot. A configuração e os fluxos técnicos aguardam verificação.

**Implicação comercial.** O JSON exportado separa o webhook autenticado de carga histórica e o agendador. Os dois acionam leituras da API do Chatwoot e gravação no MySQL. Faltam confirmar a configuração publicada e a transferência da integração para uma conta de teste. O tópico 6 trata de licenças e condições de uso comercial do n8n.

## 4. Cobertura dos eventos e histórico

**Implicação comercial.** Informar na proposta quais indicadores e períodos a solução existente consegue cobrir, incluindo os limites de atribuição por agente. Confirmar amostras de autoria, transferências, automações e pendências somente se a revisão indicar que esses detalhes afetam uma promessa ao cliente. [Campos e eventos documentados pelo Chatwoot](https://www.chatwoot.com/hc/user-guide/articles/1777049924-como-usar-webhooks)

**Ponto para a revisão técnica.** Conferir o histórico já disponível e traduzi-lo em condições comerciais de cobertura e implantação. A decisão sobre o que oferecer aguarda o material do sistema.
