import json
import re
from difflib import SequenceMatcher

class ChatbotCalasanz:
    def __init__(self, ruta_json='faq.json'):
        self.faq = self.cargar_faq(ruta_json)
        self.categorias = self.obtener_categorias()

    def cargar_faq(self, ruta_json):
        try:
            with open(ruta_json, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            return datos['faq']
        except Exception:
            print("Error al cargar el archivo JSON")
            return []

    def obtener_categorias(self):
        if not self.faq:
            return []
        return list(set(item['categoria'] for item in self.faq))

    def normalizar_texto(self, texto):
        texto = texto.lower().strip()
        texto = re.sub(r'[^\w\s]', '', texto)
        return texto

    def calcular_similitud(self, texto1, texto2):
        return SequenceMatcher(None, texto1, texto2).ratio()

    def buscar_por_palabras_clave(self, consulta_usuario):
        consulta_normalizada = self.normalizar_texto(consulta_usuario)
        palabras_consulta = set(consulta_normalizada.split())

        resultados = []

        for item in self.faq:
            palabras_clave_texto = ' '.join(item.get('palabras_clave', []))
            palabras_clave_item = set(self.normalizar_texto(palabras_clave_texto).split())
            coincidencias_clave = len(palabras_consulta.intersection(palabras_clave_item))

            pregunta_normalizada = self.normalizar_texto(item['pregunta'])
            similitud_pregunta = self.calcular_similitud(consulta_normalizada, pregunta_normalizada)

            puntuacion = coincidencias_clave * 2 + similitud_pregunta

            if puntuacion > 0.3:
                resultados.append((item, puntuacion))

        resultados.sort(key=lambda x: x[1], reverse=True)
        return resultados

    def buscar_respuesta_exacta(self, consulta_usuario):
        consulta_normalizada = self.normalizar_texto(consulta_usuario)

        for item in self.faq:
            if self.normalizar_texto(item['pregunta']) == consulta_normalizada:
                return item
        return None

    def encontrar_respuesta(self, consulta_usuario):
        respuesta_exacta = self.buscar_respuesta_exacta(consulta_usuario)
        if respuesta_exacta:
            return respuesta_exacta['respuesta'], 1.0, respuesta_exacta['categoria']

        resultados = self.buscar_por_palabras_clave(consulta_usuario)

        if resultados:
            mejor_resultado = resultados[0]
            item, puntuacion = mejor_resultado
            return item['respuesta'], puntuacion, item['categoria']

        return self.respuesta_no_encontrada(), 0.0, "general"

    def respuesta_no_encontrada(self):
        return ("Lo siento, no tengo información específica sobre esa consulta. "
                "Puedes contactar directamente al Colegio Calasanz Buenavista al "
                "teléfono 601 7920388 o visitarnos en la Carrera 17F # 77 – 75 SUR, "
                "Buenos Aires, Ciudad Bolívar.")

    def mostrar_categorias(self):
        categorias_texto = {
            'informacion_general': 'Información General',
            'ubicacion_contacto': 'Ubicación y Contacto',
            'matriculas': 'Matrículas',
            'admisiones': 'Admisiones',
            'academico': 'Información Académica',
            'horarios': 'Horarios',
            'filosofia': 'Filosofía Educativa',
            'red_colegios': 'Red de Colegios',
            'documentos': 'Documentos y Requisitos',
            'costos': 'Costos',
            'transporte': 'Transporte',
            'eventos': 'Eventos',
            'comunicacion': 'Comunicación',
            'uniforme': 'Uniforme'
        }

        texto = "\nCATEGORÍAS DISPONIBLES:\n"
        for i, categoria in enumerate(self.categorias, 1):
            nombre_categoria = categorias_texto.get(categoria, categoria.replace('_', ' ').title())
            texto += f"{i}. {nombre_categoria}\n"
        texto += "\n"
        return texto

    def procesar_consulta(self, consulta_usuario):
        if consulta_usuario.lower() in ['help', 'ayuda', 'categorias']:
            return self.mostrar_categorias()

        respuesta, puntuacion, categoria = self.encontrar_respuesta(consulta_usuario)

        if puntuacion >= 0.8:
            return respuesta
        elif puntuacion >= 0.5:
            return f"{respuesta}\n\n(Si necesitas información más específica, contacta al colegio)"
        elif puntuacion > 0:
            return f"{respuesta}\n\nTambién puedes escribir 'ayuda' para ver todas las categorías disponibles"
        else:
            return respuesta
