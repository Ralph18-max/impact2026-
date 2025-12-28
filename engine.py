import google.generativeai as genai
from fpdf import FPDF
import streamlit as st
from datetime import datetime

def generate_ai_content(raw_notes):
    """Génère le contenu en utilisant le nom de modèle standard pour éviter l'erreur 404."""
    try:
        # Configuration via les secrets Streamlit
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        
        # CORRECTION : On retire 'models/' qui causait l'erreur 404 dans tes PDF
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Tu es un Expert en Rétention Client et Stratège Business. 
        Transforme ces notes brutes en un rapport d'impact annuel prestigieux.
        
        Notes : {raw_notes}
        
        STRUCTURE STRICTE :
        TITRE: Un titre percutant sur la croissance.
        BILAN: 3 à 5 points clés (verbes d'action).
        VALEUR: Pourquoi ce travail est un investissement rentable (ROI).
        VISION: Une recommandation stratégique pour 2026.
        
        Ton : Professionnel, convaincant, français impeccable.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # Gestion propre des erreurs de quota ou technique
        if "429" in str(e):
            return "Erreur : Quota Google dépassé (trop de demandes). Réessayez dans 1 minute."
        return f"Erreur de génération : {str(e)}"

class ImpactPDF(FPDF):
    def header(self):
        # Récupération de la date du jour pour l'en-tête
        date_aujourdhui = datetime.now().strftime("%d/%m/%Y")
        
        self.set_fill_color(41, 128, 185)
        self.rect(0, 0, 210, 20, 'F')
        
        # Titre Principal
        self.set_font('helvetica', 'B', 12)
        self.set_text_color(255, 255, 255)
        self.cell(0, 8, "RAPPORT D'IMPACT ANNUEL 2025", 0, 1, 'C')
        
        # Phrase du contrat avec la date dynamique
        self.set_font('helvetica', 'I', 9)
        self.cell(0, 5, f"Relatif au rapport du contrat du {date_aujourdhui}", 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, 'Généré par Impact-2026 - Document Confidentiel', 0, 0, 'C')

def create_pdf(freelance, client_name, content, is_pro=False):
    pdf = ImpactPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    if not is_pro:
        pdf.set_font("helvetica", 'B', 40)
        pdf.set_text_color(230, 230, 230)
        with pdf.rotation(45, 100, 150):
            pdf.text(40, 150, "SPECIMEN - VERSION GRATUITE")

    pdf.ln(15)
    pdf.set_font("helvetica", 'B', 11)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(0, 8, f"PRESTATAIRE : {freelance.upper()}", ln=True)
    pdf.cell(0, 8, f"CLIENT : {client_name.upper()}", ln=True)
    pdf.ln(10)

    pdf.set_font("helvetica", '', 11)
    pdf.set_text_color(0, 0, 0)
    
    # Encodage latin-1 pour FPDF (évite les bugs sur les accents)
    clean_content = content.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 8, clean_content)
    
    output_path = f"rapport_{client_name.replace(' ', '_')}.pdf"
    pdf.output(output_path)
    return output_path