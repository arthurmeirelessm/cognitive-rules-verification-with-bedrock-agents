import json
import os
from typing import Any, Dict, List, Optional

import boto3
from beartype import beartype
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.types import TypeDeserializer
from dotenv import load_dotenv

from src.logger import log_execution

load_dotenv()


class DynamoDbClientRepository:
    def __init__(self):
        self.dynamodb = boto3.client("dynamodb", region_name="us-east-1")
        self.table = os.getenv("DYNAMO_DB_TABLE")
        
        

    async def get_all(self):
        """
        Busca todos os itens da tabela no DynamoDB e os converte para JSON.
        """
        try:
            response = self.dynamodb.scan(TableName=self.table, Select="ALL_ATTRIBUTES")
            items = response.get("Items", [])
            print(items)
            formatted_items = [{k: v[list(v.keys())[0]] for k, v in item.items()} for item in items]

            return json.dumps(
                formatted_items, ensure_ascii=False
            ) 
        except Exception as e:
            print(f"Erro ao buscar itens: {e}")
            return json.dumps([])
        
        

    @log_execution
    @beartype
    async def create_item(self, cpf: str, email: str, nome: str, celular: str) -> bool:
        """
        Insere um novo item na tabela DynamoDB.

        :param cpf: CPF do usuário (chave primária)
        :param email: Email do usuário
        :param nome: Nome do usuário
        :param celular: Número de celular do usuário
        :return: O item criado, ou None em caso de erro
        """
        print(f"self.table: {self.table}")

        try:
            self.dynamodb.put_item(
                TableName=self.table,
                Item={
                    "cpf": {"S": cpf},
                    "email": {"S": email},
                    "nome": {"S": nome},
                    "celular": {"S": celular},
                },
            )
            return True
        except Exception as e:
            print(f"Erro ao criar item: {e}")
            return False
