# Prompt para o Claude

Implemente a aba **Monte sua solução** no site público da frente de tecnologia da Norte Pioneiro Engenharias. O visitante deve ver o que a base de analytics inclui, escolher adicionais, entender dependências e enviar um resumo para solicitar uma proposta. A equipe comercial trata investimento, implantação e mensalidade diretamente com o cliente. A página, o catálogo público e o resumo ficam sem preços, faixas de preço, simulações, subtotais ou totais monetários. Escreva a interface em português do Brasil e mantenha a identidade visual da área tech. O nome comercial da divisão deve vir da configuração já usada no site.

## Escopo e ponto de partida

- Examine apenas as instruções do repositório do site, os manifestos, as rotas, o layout, a navegação, os estilos e os componentes que você precisa reutilizar. Pule dependências geradas, builds, históricos, arquivos de ambiente com segredos, dumps e dados pessoais.
- Crie uma rota pública como `/monte-sua-solucao` e um link na navegação da área tech. Adapte a rota ao padrão do site. Se o projeto for HTML/CSS/JS estático, faça uma implementação estática. Se já houver framework, mantenha a estrutura e a hospedagem compatíveis.
- A aba é parte da landing comercial. Mantenha o catálogo e as regras de seleção desacoplados do painel de atendimento, de sua API, do n8n e do banco. O projeto desta aba termina no resumo e no pedido de proposta. Pagamento, login comercial e ativação de módulos são etapas posteriores.
- Use somente conteúdo, identidade e exemplos próprios da oferta pública. Dados reais, nomes de atendentes, credenciais, marcas e ativos do projeto de origem estão fora do conteúdo da página.

## Conteúdo e interações

1. Mostre a **Base Analytics para Chatwoot** já incluída na configuração. Explique que ela cobre volume por horário, primeira resposta, pendências, visão por agente conforme a cobertura, filtros e exportação XLSX. Use linguagem direta e curta.
2. Peça apenas o necessário para indicar escopo: plataforma atual, número de caixas/equipes, faixa de conversas por mês e se há pedido de histórico anterior. Não solicite token do Chatwoot, exemplos de conversa ou outros dados operacionais. Trate “não sei” como uma opção válida.
3. Mostre módulos em cartões selecionáveis. Cada cartão apresenta resultado, condições e status. Use controles nativos ou equivalentes acessíveis. Explique por que algo depende de validação.
4. Mantenha um resumo visível no desktop e de fácil acesso no celular. Mostre itens da base, adicionais, quantidades, contexto da operação e itens pendentes de avaliação. Use uma frase como “Nossa equipe confirma o escopo e apresenta a proposta em contato direto”.
5. Forneça **Solicitar proposta** para o canal oficial configurado no site e **Copiar resumo** como alternativa. O resumo deve conter plataforma, faixa de conversas, caixas/equipes, histórico pedido, módulos escolhidos e condições pendentes. Use apenas o canal de contato real já configurado. Enquanto ele estiver ausente, ofereça a cópia com feedback claro. Encode adequadamente a mensagem se houver link de WhatsApp ou e-mail.

## Catálogo inicial

| Item | Como apresentar |
| --- | --- |
| Base Analytics para Chatwoot | Incluída na configuração. A cobertura depende da origem autorizada. |
| Caixa adicional | Registrar quantidade desejada para uma operação Chatwoot. A equipe confirma capacidade, franquia e implantação na conversa comercial. |
| Gestão de metas e auditoria | Candidato a módulo. A versão analisada tem meta de primeira resposta definida pelo cliente, tendência da equipe, papel de gestor e auditoria administrativa. Exibir “Sob consulta” até validar instalação, controle de acesso e pacote comercial. |
| Classificação por IA | Adicional optativo sob consulta. Exige aprovação do tratamento de conteúdo e validação de consumo. |
| Histórico adicional ou integração com outra plataforma | Adicionar como necessidade no pedido, sob diagnóstico. Para plataforma diferente, indicar que a compatibilidade precisa ser avaliada. |
| Assistente com documentos e busca por IA | RAG é uma oferta futura em avaliação. Pode aparecer como interesse sob consulta. |

Defina o catálogo em um único arquivo ou estrutura equivalente. Parâmetros úteis são ID estável, título, descrição, status comercial, limites de quantidade, unidade operacional e dependências. Mantenha a tabela interna de preços fora do projeto público, inclusive do HTML, dos dados do catálogo, dos bundles e da mensagem enviada. Nenhum cálculo financeiro é necessário para esta aba.

## Validação das escolhas e experiência

- Valide mínimo, máximo, inteiros, compatibilidade e dependências. Ao mudar a origem, explique qualquer seleção que fique pendente ou incompatível e atualize o resumo. Evite itens duplicados e preserve os itens sob consulta no texto enviado.
- Use uma composição visual com lista de opções e resumo lateral. No celular, coloque o resumo após as escolhas e garanta acesso fácil ao botão de proposta, sem cobrir conteúdo. Reutilize cores, tipografia e componentes da área tech. Use estados claramente diferentes para incluído, selecionável, sob consulta e futuro. Use texto ou ícone acompanhado de rótulo, sem depender só de cor.
- Garanta uso por teclado, foco visível, rótulos associados, contraste, alvos de toque e leitura do resumo por tecnologia assistiva. Use anúncios discretos para mudanças importantes e mensagens compreensíveis em campos inválidos. Mantenha o fluxo funcional com preferências de movimento reduzido.
- Pela hospedagem prevista, prefira configuração local e implantação estática quando o projeto permitir. A seleção registra o interesse do visitante e fica sujeita à confirmação de escopo.

## Verificação e entrega

- Teste base sozinha, seleção de caixas, entradas inválidas, módulo sob consulta, origem fora do catálogo, reversão de seleção, copiar resumo e contato configurado ou ausente.
- Confira se o resumo distingue módulos selecionados e itens para avaliação. Verifique que página, catálogo, bundle e mensagem permanecem sem dados de preço.
- Verifique desktop e celular, teclado, CTA e ausência de contatos fictícios. Execute as checagens do projeto e adicione testes das regras de seleção quando a estrutura suportar.
- Entregue a rota integrada ao menu e diga quais arquivos mudaram, onde ajustar catálogo e contato e quais verificações você executou. Mantenha a implementação local. A publicação é aprovada pelo responsável comercial.
