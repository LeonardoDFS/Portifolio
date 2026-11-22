# Visão do produto

## Problema e oferta

O gestor de atendimento precisa saber onde conversas esperam, quando reforçar a escala e se o ajuste funcionou. Quando os dados ficam dispersos ou o relatório da ferramenta não responde a essas perguntas, ele depende de amostras manuais e descobre gargalos tarde.

**Produto 1 | Analytics e Automação de Atendimento.** Serviço recorrente com implantação. Lê dados autorizados da operação existente, transforma eventos em indicadores comparáveis e entrega painel, revisão das métricas e automações de acompanhamento. O decisor é quem responde pela fila ou pelo resultado da unidade. O usuário diário é o gestor de atendimento.

**Produto 2 | IA e RAG.** Projeto premium facultativo, com implantação e operação próprias. Busca semântica e assistentes consultam documentos autorizados, ajudam atendentes com sugestões e podem classificar e resumir conversas. A operação do Produto 1 pode ser contratada independentemente. O primeiro projeto de IA depende de conteúdo confiável, patrocínio e orçamento. [Viabilidade e critérios](product-2-rag.md)

## Entrega proposta do Produto 1

- Sincronizar eventos autorizados e apresentar histórico disponível, com período coberto e estado da coleta.
- Medir volume, primeira resposta humana, intervalos entre turnos, picos, fila aberta, casos sem resposta e métricas por equipe e atendente quando a fonte permitir atribuição.
- Filtrar por período, horário, unidade, canal, fila, status e equipe, com histórico em nível de conversa conforme autorização e cobertura da fonte.
- Oferecer resumo programado e alerta de ausência de resposta com responsável e regra de supressão. Usar P50/P90 e backlog por faixa de espera para localizar gargalos, com amostras e contexto de escala.
- Preservar a operação do cliente na sua ferramenta, com dashboard de acesso restrito e exportação dos indicadores contratados. Recursos como inbox, CRM, disparos, ranking automático e novos conectores ficam fora do primeiro piloto.

**Rotina real de uso.** Na segunda-feira, um gestor filtra as primeiras respostas nas duas unidades e percebe concentração de esperas na troca de turno. Abre uma amostra de casos, confirma o padrão e ajusta a cobertura. Na semana seguinte, compara o P90 e o volume de entradas nos mesmos horários. A comparação registra a mudança, com atribuição causal ainda dependente do desenho do teste.

## O que sabemos sobre a solução original

O proponente informa que o sistema está pronto e funcional, com melhorias e implementações em andamento. O pedido descreve coleta, armazenamento, processamento de indicadores e dashboard web em uma operação real. O PDF atribui à solução coleta incremental via n8n, filtros e consulta a histórico. O estado de cada recurso será verificado quando houver material técnico autorizado. As funcionalidades descritas acima orientam a oferta e não constituem inventário técnico. O uso comercial dos componentes existentes depende da verificação de direitos e licenças.

## Indicadores de validação

- **Adoção:** gestor consulta indicadores em pelo menos três das quatro semanas do piloto e registra duas decisões operacionais.
- **Confiança:** critérios de cobertura, conciliação, latência e atribuição acordados antes de começar. [Roadmap e dicionário](product-1-roadmap.md)
- **Resultado:** demonstrar indicadores como P90 de primeira resposta e conversas aguardando retorno, com volume e horário como contexto. O cliente decide como usar os indicadores e se quer definir metas internas.
- **Negócio:** interesse verificável em piloto pago, disposição para mensalidade, horas reais de suporte e possibilidade de repetir a implantação.
