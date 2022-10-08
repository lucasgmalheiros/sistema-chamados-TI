# Sistema de Chamados de Serviços em TI

Esse protótipo foi desenvolvido para a matéria de sistemas de informações gerencias 
do curso de engenharia de produção da Universidade Federal de São Carlos (UFSCar).

## Motivação e Funcionalidades

A proposta do projeto era desenvolver um software que gerenciasse as solicitações de serviços de 
tecnologia da informação realizados dentro do Departamento de Engenharia de Produção. O sistema deveria 
apresentar aos solicitantes uma fila de solicitações, organizá-la por prioridade de atendimento e permitir
acompanhar o andamento das solicitações em tempo real. Os técnicos de informática, responsáveis pelo atendimento do serviço,
poderiam acompanhar todas as demandas em andamento, as concluídas, e ainda atualizar informações relevantes, principalmente
o status do atendimento do chamado. O último ator do sistema é o coordenador de informática, que além das funcionalidades dos solicitantes
ainda pode consultar relatórios contendo informações gerenciais.

Todas as funcionalidades resumidas acima estão descritas no diagrama de casos de uso (DCU).

## Desenvolvimento

As ferramentas utilizadas foram: Figma, para design da interface gráfica, MySQL, como banco de dados, e Python, para programação
de todo o software. O projeto Tkinter-Designer (https://github.com/ParthJadhav/Tkinter-Designer) 
foi fundamental para agilizar a modelagem gráfica da interface em Python, gerando os códigos das telas pela biblioteca Tkinter,
integrando-se à API do Figma.

## Funcionamento
Para utilizar o protótipo basta criar um banco de dados em MySQL com o modelo físico presente no arquivo
**conecta_banco.py** e realizar a conexão com o Python, alterando os argumentos contidos na funcão **ConectaBanco**.
A partir daí, basta executar **telas.py** para utilizar a interface gráfica, os usuários já podem ser cadastrados pela GUI 
e todas as informações do sistema serão atualizadas no banco de dados.
