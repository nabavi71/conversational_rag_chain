import weaviate
from weaviate.classes.config import DataType, Property, Configure
from weaviate.classes.init import Auth
from traceback import format_exc
import csv


class WeaviateConnect:

    def __init__(self, config):

        self.config = config

    def connect(self):

        if self.config.api_key:
            auth_config = Auth.api_key(self.config.api_key)
        else:
            auth_config = None

        try:

            self.client = weaviate.connect_to_local(
                host= self.config.host,
                port= self.config.port,
                auth_credentials= auth_config)

            print(f"connection to {self.config.host} successfully")
            return self.client

        except:
            print(f"Weaviate Connection Failed:\n\n{format_exc()}")

        return self.client


    def create_schema(self):

        try:

            schema = self.client.collections.create(
                name="famous_people",
                vectorizer_config= Configure.Vectorizer.text2vec_transformers(),
                generative_config= Configure.Generative.cohere(),
                description="Information about famous people in the world",
                properties=[
                    Property(
                        name="URI",
                        data_type=DataType.TEXT
                    ),
                    Property(
                        name="name",
                        data_type=DataType.TEXT
                    ),
                    Property(
                        name="text",
                        data_type=DataType.TEXT
                    )
                ]

            )

            print(schema.config.get(simple=False))

        except:
            print(f"Weaviate Collection Failed:\n\n{format_exc()}")

        finally:
            self.client.close()


    def read_csv(self, csv_path):

        with open(csv_path, mode='r', encoding='utf_8') as file:

            data = csv.DictReader(file)
            records = [rec for rec in data]

            return records


    def insert_data(self, csv_path):

        data = self.read_csv(csv_path)
        batch_size = 100
        self.client.batch.batch_size=batch_size
        collection = self.client.collections.get(name='famous_people')


        with collection.batch.dynamic() as batch:
            for i, record in enumerate(data):

                batch.add_object(
                    properties=record,
                    )

                if (i + 1) % 100 == 0:
                    print(f"{i + 1} records added to Weaviate...")

        self.client.close()