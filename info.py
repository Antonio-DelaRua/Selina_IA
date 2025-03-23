

class CompanyInfo:
    NOTION_API_KEY = "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"
    NOTION_DATABASE_ID = "1bef4868-0df1-80e4-9707-cc0d1af9cd1d"

    NOMBRE =  "NoBt Shop"
    EMPRESA = "Desarrollo de software y soluciones IA"
    MISSION = "Brindar soluciones innovadoras basadas en inteligencia artificial para optimizar procesos empresariales."
    VISION =  "Ser la empresa líder en IA aplicada a la automatización y análisis de datos."
    VALORES =["Innovación", "Calidad", "Transparencia", "Compromiso", "Eficiencia"]

    SERVICIOS = [
        "Desarrollo de software a medida",
        "Implementación de inteligencia artificial",
        "Optimización de procesos con automatización",
        "Análisis de datos y predicciones con machine learning",
        "Consultoría en transformación digital"
    ]

    CONTACTO = {
        "email": "contacto@tNoBt.com",
        "telefono": "+34 600 123 456",
        "direccion": "Calle Innovación 123, Madrid, España",
        "sitio_web": "https://www.NoBt.com"
    }

    EQUIPO = [
        {"nombre": "Antonio De la Rua", "rol": "CEO", "experiencia": "15 años en tecnología y negocios"},
        {"nombre": "Juan de Aranzadi", "rol": "CTO", "experiencia": "Experta en IA y Machine Learning"},
        {"nombre": "Daniel Urbano", "rol": "COO", "experiencia": "Especialista en operaciones y escalabilidad"}
    ]

    FAQS = {
        "ubicación": "Nuestra sede está en Madrid, España, pero ofrecemos servicios a nivel global. 🌍",
        "clientes": "Trabajamos con empresas de todos los tamaños, desde startups hasta corporaciones. 🏢➡️🏭",
        "contratación": "Puedes contactarnos por correo electrónico o a través de nuestra web. 📩🌐"
    }

    @classmethod
    def get_info(cls):
        """
        Devuelve toda la información corporativa estructurada
        """
        return f"""
        **{cls.NOMBRE}** - _{cls.EMPRESA}_ 🚀

        📌 **Misión:**  
        {cls.MISSION}

        🔭 **Visión:**  
        {cls.VISION}

        💎 **Valores:**  
        {', '.join(cls.VALORES)}  

        🛠 **Servicios Principales:**  
        {chr(10).join(['• ' + servicio for servicio in cls.SERVICIOS])}

        📞 **Contacto:**  
        ✉️ {cls.CONTACTO["email"]}  
        📱 {cls.CONTACTO["telefono"]}  
        🏠 {cls.CONTACTO["direccion"]}  
        🌐 [{cls.CONTACTO["sitio_web"]}]({cls.CONTACTO["sitio_web"]})
        """

    @classmethod
    def get_team(cls):
        """
        Devuelve información del equipo con formato mejorado
        """
        return "\n".join(
            [f"👤 **{member['nombre']}** - _{member['rol']}_\n   📌 {member['experiencia']}" 
             for member in cls.EQUIPO]
        )

if __name__ == "__main__":
    print(CompanyInfo.get_info())
    print("\n🔹 Equipo:\n" + CompanyInfo.get_team())