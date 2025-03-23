from notion_client import Client
from info import CompanyInfo  # Asegúrate de que este archivo contiene las credenciales correctas


class NotionDB:
    @staticmethod
    def query_database(prompt: str):
        try:
            notion = Client(auth=CompanyInfo.NOTION_API_KEY)

            query_result = notion.databases.query(
                database_id=CompanyInfo.NOTION_DATABASE_ID,
                filter={"property": "prompt", "rich_text": {"equals": prompt}}
            )

            print(f"📌 DEBUG - Respuesta de Notion: {query_result}")  # 👀 Verifica la estructura

            if query_result.get("results"):  # Se corrige `notion_results` a `query_result`
                page = query_result["results"][0]  # Primer resultado
                respuesta = page["properties"]["respuesta"]["rich_text"]

                # Extrae el texto si existe
                if respuesta:
                    respuesta_texto = respuesta[0]["plain_text"]
                else:
                    respuesta_texto = "No hay respuesta disponible."

                print(f"📌 Respuesta encontrada: {respuesta_texto}")
            else:
                respuesta_texto = "No se encontraron resultados en Notion."

            # Retorna la respuesta final
            return respuesta_texto

        except Exception as e:
            print(f"⚠️ Error en la consulta a Notion: {e}")
            return "Error al consultar la base de datos."

    @staticmethod
    def extract_page_content(notion, page_id):
        """
        Extrae contenido estructurado de una página de Notion
        """
        try:
            blocks = notion.blocks.children.list(block_id=page_id)
            respuesta = []
            for block in blocks.get("results", []):
                if block["type"] == "paragraph":
                    text = "".join([t["plain_text"] for t in block["paragraph"]["rich_text"]])
                    respuesta.append(text)
            return "\n".join(respuesta)

        except Exception as e:
            print(f"⚠️ Error extrayendo contenido de la página: {e}")
            return ""