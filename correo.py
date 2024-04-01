import smtplib
import ssl
from email.message import EmailMessage
import pandas as pd
from datetime import datetime
import time
import streamlit as st

def variables_entrada():
# Breve descripción o instrucción para el usuario
    col1, col2 ,col3 = st.columns((1,5,1))
    col2.write("")
    col2.markdown("##### Por favor, completa los siguientes campos para enviar tu postulación.")
    
    # Usa un contenedor para alinear tus inputs
    with col2.container():
        # Añade algo de espacio antes del primer input
        st.write("")  # Este es simplemente un espacio en blanco para mejor estética
        
        # Solicitar la dirección de correo del receptor
        receptores = st.text_input("Correo del Receptor:", placeholder="ejemplo@dominio.com")

        # Solicitar el puesto de trabajo
        puesto = st.text_input("Puesto de Postulación:", placeholder="Nombre del Puesto")
        
        # Solicitar el asunto del correo
        asunto = st.text_input("Asunto del Correo:", placeholder="Asunto del Correo")

    return receptores, puesto, asunto

def enviar_email(archivo_adjunto,receptores, puesto, asunto):
    fecha_actual = datetime.now()
    fecha_formateada = fecha_actual.strftime("%d/%m/%Y")
    hora_actual = datetime.now().time()
    if hora_actual.hour < 12:
        saludo = "Buenos Dias"
    else:
        saludo = "Buenas Tardes"
    emisor = 'gustavoboadalugo@gmail.com'  # Cambia esto por tu dirección de correo Gmail
    clave = st.secrets["Clave"] 
 # Cambia esto por tu contraseña de correo Gmail
    cuerpo_html = f"""
    <html>
        <head>
            <style>
                body {{
                    text-align: justify;
                }}
                p {{
                    margin-bottom: 20px;
                }}
            </style>
        </head>
        <body>
            <h3>{saludo}</h3>
            <h4>Estimado reclutadores, reciban un cordial saludo.</h4>
            <p>Me permito presentarme como candidato al puesto de {puesto}, motivado por mi 
            formación en Ciencias Actuariales y una sólida base en estadistica y el análisis de datos. 
            Actualmente curso el 8vo semestre de mi carrera y tengo experiencia práctica con herramientas como 
            SQL, Python, Power BI, Looker Studio y Google BigQuery. Mi educación y proyectos 
            personales me han dotado de la habilidad para transformar datos complejos en decisiones estratégicas claras.</p> 

            <p>Mi CV adjunto ofrece una visión detallada de mis habilidades técnicas y proyectos personales.
            Estoy seguro de que mi perfil puede aportar valor a su equipo, y estoy deseoso
            de explorar cómo puedo contribuir a sus objetivos.</p> 

            <p>Agradezco su tiempo y consideración, y quedo a la espera de la oportunidad 
            de discutir mi aplicación en detalle. </p>

            <h5>Tlf: 04126050917 / 04141240654</h5>
        </body>
    </html>
    """

    # Asegúrate de reemplazar 'saludo' y 'puesto' con las variables o valores correspondientes

    em = EmailMessage()
    em["From"] = emisor
    em["To"] = receptores
    em["Subject"] = asunto
    em.add_alternative(cuerpo_html, subtype='html')

    # Leer el contenido del archivo PDF cargado desde el uploader
    archivo = archivo_adjunto.read()
    em.add_attachment(archivo, maintype="application", subtype="pdf", filename=f"CV GUSTAVO BOADA.pdf")

    contexto = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexto) as smtp:
            smtp.login(emisor, clave)
            smtp.sendmail(emisor, receptores, em.as_string())
    except Exception as e:
        st.error(f"Error al enviar el correo electrónico: {str(e)}")

def main():
    st.markdown(
    """<div style= padding: 5px; border-radius:5px;'>
    <span style='color: ##1D20FA; font-size: 3.5em;'><center><b>Enviar Cv a los reclutadores</center></span>
    </div>""",unsafe_allow_html=True)
    receptores, puesto, asunto = variables_entrada() 
    col1, col2 ,col3 = st.columns((1,5,1))
    uploaded_file = col2.file_uploader("Carga el Cv en archivo PDF", type=["pdf"])
    b1, sub2, sub3 = st.columns((4,2,4))
    if uploaded_file is not None:
        if sub2.button("Enviar correo"):
            col1, col2, col3 = st.columns((1,4,1))
            enviar_email(uploaded_file,receptores=receptores, puesto=puesto,asunto=asunto)
            col2.success("Postulacion enviada con exito")

if __name__ == "__main__":
    main()