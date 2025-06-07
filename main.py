import json
import re
from difflib import SequenceMatcher

class ChatbotCalasanz:
    def __init__(self, ruta_json='faq.json'):
        self.faq = self.cargar_faq(ruta_json)
        self.categorias = self.obtener_categorias()
    
    def cargar_faq(self, ruta_json):
        """Carga las preguntas frecuentes desde un archivo JSON."""
        try:
            with open(ruta_json, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            return datos['faq']
        except Exception:
            print("Error al cargar el archivo JSON")
            return []
    
    def obtener_categorias(self):
        """Obtiene todas las categorías disponibles."""
        if not self.faq:
            return []
        return list(set(item['categoria'] for item in self.faq))
    
    def normalizar_texto(self, texto):
        """Normaliza el texto para facilitar la coincidencia. hola"""
        texto = texto.lower().strip()
        texto = re.sub(r'[^\w\s]', '', texto)
        return texto
    
    def calcular_similitud(self, texto1, texto2):
        """Calcula la similitud entre dos textos."""
        return SequenceMatcher(None, texto1, texto2).ratio()
    
    def buscar_por_palabras_clave(self, consulta_usuario):
        """Busca respuestas basándose en palabras clave."""
        consulta_normalizada = self.normalizar_texto(consulta_usuario)
        palabras_consulta = set(consulta_normalizada.split())
        
        resultados = []
        
        for item in self.faq:
            # Buscar en palabras clave
            palabras_clave_texto = ' '.join(item.get('palabras_clave', []))
            palabras_clave_item = set(self.normalizar_texto(palabras_clave_texto).split())
            coincidencias_clave = len(palabras_consulta.intersection(palabras_clave_item))
            
            # Buscar en la pregunta
            pregunta_normalizada = self.normalizar_texto(item['pregunta'])
            similitud_pregunta = self.calcular_similitud(consulta_normalizada, pregunta_normalizada)
            
            # Calcular puntuación total
            puntuacion = coincidencias_clave * 2 + similitud_pregunta
            
            if puntuacion > 0.3:
                resultados.append((item, puntuacion))
        
        # Ordenar por puntuación descendente
        resultados.sort(key=lambda x: x[1], reverse=True)
        return resultados
    
    def buscar_respuesta_exacta(self, consulta_usuario):
        """Busca una respuesta con coincidencia exacta."""
        consulta_normalizada = self.normalizar_texto(consulta_usuario)
        
        for item in self.faq:
            if self.normalizar_texto(item['pregunta']) == consulta_normalizada:
                return item
        return None
    
    def encontrar_respuesta(self, consulta_usuario):
        """Encuentra la mejor respuesta para la consulta del usuario."""
        # Primero intentar coincidencia exacta
        respuesta_exacta = self.buscar_respuesta_exacta(consulta_usuario)
        if respuesta_exacta:
            return respuesta_exacta['respuesta'], 1.0, respuesta_exacta['categoria']
        
        # Luego buscar por palabras clave y similitud
        resultados = self.buscar_por_palabras_clave(consulta_usuario)
        
        if resultados:
            mejor_resultado = resultados[0]
            item, puntuacion = mejor_resultado
            return item['respuesta'], puntuacion, item['categoria']
        
        return self.respuesta_no_encontrada(), 0.0, "general"
    
    def respuesta_no_encontrada(self):
        """Respuesta cuando no se encuentra información."""
        return ("Lo siento, no tengo información específica sobre esa consulta. "
                "Puedes contactar directamente al Colegio Calasanz Buenavista al "
                "teléfono 601 7920388 o visitarnos en la Carrera 17F # 77 – 75 SUR, "
                "Buenos Aires, Ciudad Bolívar.")
    
    def mostrar_categorias(self):
        """Muestra las categorías disponibles."""
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
        
        print("\nCATEGORIAS DISPONIBLES:")
        for i, categoria in enumerate(self.categorias, 1):
            nombre_categoria = categorias_texto.get(categoria, categoria.replace('_', ' ').title())
            print(f"{i}. {nombre_categoria}")
        print()
    
    def procesar_consulta(self, consulta_usuario):
        """Procesa la consulta del usuario y devuelve la respuesta formateada."""
        # Comandos especiales
        if consulta_usuario.lower() in ['help', 'ayuda', 'categorias']:
            self.mostrar_categorias()
            return "Sobre que categoria te gustaria conocer mas?"
        
        # Buscar respuesta
        respuesta, puntuacion, categoria = self.encontrar_respuesta(consulta_usuario)
        
        # Formatear respuesta según la puntuación
        if puntuacion >= 0.8:
            return respuesta
        elif puntuacion >= 0.5:
            return f"{respuesta}\n\n(Si necesitas informacion mas especifica, contacta al colegio)"
        elif puntuacion > 0:
            return f"{respuesta}\n\nTambien puedes escribir 'ayuda' para ver todas las categorias disponibles"
        else:
            return respuesta


def main():
    print("CHATBOT COLEGIO CALASANZ BUENAVISTA")
    print("=" * 50)
    print("Hola! Soy el asistente virtual del Colegio Calasanz Buenavista.")
    print("Puedo ayudarte con informacion sobre matriculas, admisiones, ubicacion y mas.")
    print("Escribe 'ayuda' para ver las categorias disponibles.")
    print("Escribe 'salir' para terminar.")
    print("=" * 50)
    
    chatbot = ChatbotCalasanz('faq.json')
    
    if not chatbot.faq:
        print("No se pudo cargar la base de preguntas frecuentes. Saliendo.")
        return
    
    while True:
        print("\n" + "-" * 50)
        consulta_usuario = input("Tu: ").strip()
        
        if consulta_usuario.lower() in {'salir', 'exit', 'quit', 'bye'}:
            print("Bot: Hasta luego! Gracias por usar el chatbot del Colegio Calasanz Buenavista.")
            break
        
        if not consulta_usuario:
            print("Bot: Por favor escribe tu consulta.")
            continue
        
        respuesta = chatbot.procesar_consulta(consulta_usuario)
        print(f"Bot: {respuesta}")


if __name__ == '__main__':
    main()