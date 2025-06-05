- Criação da tabela 'usuarios'
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    localizacao VARCHAR(255),
    tipo_perfil ENUM('pessoa', 'ong') NOT NULL,
    bloqueado BOOLEAN DEFAULT FALSE
);

-- Criação da tabela 'alimentos'
CREATE TABLE alimentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    validade DATE NOT NULL,
    quantidade INT NOT NULL,
    doador_id INT,
    FOREIGN KEY (doador_id) REFERENCES usuarios(id)
);

-- Criação da tabela 'retiradas'
CREATE TABLE retiradas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    alimento_id INT,
    data DATE,
    local VARCHAR(255),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (alimento_id) REFERENCES alimentos(id)
);

-- Criação da tabela 'perfis'
CREATE TABLE perfis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    descricao VARCHAR(255) NOT NULL
);

-- Criação da tabela 'avaliacoes'
CREATE TABLE avaliacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    nota INT NOT NULL,
    comentario TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- Inserindo dados de exemplo
INSERT INTO usuarios (nome, email, tipo_perfil, localizacao, bloqueado) VALUES
('João Silva', 'joao@example.com', 'pessoa', 'São Paulo', FALSE),
('Maria Oliveira', 'maria@example.com', 'ong', 'Rio de Janeiro', FALSE);

-- Agora vamos verificar os IDs que foram gerados para João e Maria
-- Geralmente, serão 1 e 2, respectivamente

INSERT INTO alimentos (nome, validade, quantidade, doador_id) VALUES
('Arroz', '2025-06-30', 100, 1),  -- doador_id 1 = João Silva
('Feijão', '2025-07-10', 50, 2);  -- doador_id 2 = Maria Oliveira

INSERT INTO retiradas (usuario_id, alimento_id, data, local) VALUES
(2, 1, '2025-06-15', 'Rio de Janeiro');  -- usuário 2 (Maria) retirando alimento 1 (Arroz)

-- Se quiser conferir os usuários cadastrados:
SELECT id, nome, email FROM usuarios;

-- Resetar bloqueio (não precisa se inserir com FALSE, mas só pra garantir)
SET SQL_SAFE_UPDATES = 0;
UPDATE usuarios SET bloqueado = FALSE;
SET SQL_SAFE_UPDATES = 1;