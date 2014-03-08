create table bares (
  id integer primary key autoincrement,
  nome text not null,
  descricao text not null,
  imagem text,
  endereco text not null,
  telefone text not null,
  especialidade text not null
);