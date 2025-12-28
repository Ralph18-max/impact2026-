import streamlit as st
from engine import generate_ai_content, create_pdf
import os

st.set_page_config(page_title="Impact-2026 | Sécurisez vos contrats", layout="centered")

st.title("🚀 Impact-2026")
st.subheader("Transformez votre travail de 2025 en un contrat pour 2026.")
st.markdown("🎁 **Offre de lancement :** L'outil est 100% gratuit aujourd'hui !")

# Formulaire d'entrée
with st.form("report_form"):
    col1, col2 = st.columns(2)
    with col1:
        freelance_name = st.text_input("Votre nom/entreprise", placeholder="Ex: Jean Kouassi")
    with col2:
        client_name = st.text_input("Nom du client", placeholder="Ex: Entreprise XYZ")
    
    raw_tasks = st.text_area(
        "Qu'avez-vous accompli cette année ? (Notes en vrac)", 
        placeholder="Ex: J'ai géré les réseaux sociaux, fait 12 visuels, augmenté les abonnés de 15%..."
    )
    
    submit = st.form_submit_button("Générer mon rapport pro")

if submit:
    if not raw_tasks or not freelance_name or not client_name:
        st.error("Veuillez remplir tous les champs pour générer le rapport.")
    else:
        with st.spinner("L'IA analyse votre impact et rédige le document..."):
            enhanced_content = generate_ai_content(raw_tasks)
            pdf_path = create_pdf(freelance_name, client_name, enhanced_content, is_pro=True)

            st.success("✅ Votre rapport est prêt !")
            st.balloons()

            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="📥 Télécharger mon Rapport Strategic (PDF)",
                    data=f,
                    file_name=os.path.basename(pdf_path),
                    mime="application/pdf"
                )

            st.info("💡 Si cet outil vous a aidé, partagez-le avec d'autres freelances !")
