# Pulumi

Ferramentas usadas:

- [Python](https://www.python.org/)
- [uv](https://docs.astral.sh/uv)
- [AWS CLI](https://aws.amazon.com/cli/)
- [Pulumi](https://www.pulumi.com/)

## Execução

Variáveis de ambiente necessárias:

- `AWS_ACCESS_KEY_ID`: identificador da chave de acesso da AWS.
- `AWS_SECRET_ACCESS_KEY`: chave secreta de acesso da AWS.
- `AWS_DEFAULT_REGION`: região padrão da AWS.
- `PULUMI_ACCESS_TOKEN`: *token* de acesso do Pulumi.

Criar *stack* do Pulumi:

```bash
pulumi new python --dir pulummi
```

Iniciar:

```bash
pulumi up
```

Terminar:

```bash
pulumi destroy
```

## Referências

- [The Twelve-Factor App](https://12factor.net)
