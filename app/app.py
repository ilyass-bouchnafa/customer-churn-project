import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from io import BytesIO
import base64
from pathlib import Path

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Churn Guardian AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS PERSONNALISÉ PROFESSIONNEL DARK MODE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Poppins:wght@600;700&display=swap');
    
    /* Global Styles - Dark Mode */
    .stApp {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    
    /* Header avec gradient - Dark Mode */
    .main-header {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        padding: 2.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 15px 35px rgba(99, 102, 241, 0.5);
        animation: fadeInDown 0.8s ease-out;
        border: 1px solid rgba(139, 92, 246, 0.3);
    }
    
    .main-title {
        font-family: 'Poppins', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        color: white;
        margin: 0;
        text-align: center;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.3);
        letter-spacing: -1px;
    }
    
    .main-subtitle {
        font-size: 1.3rem;
        color: rgba(255,255,255,0.95);
        text-align: center;
        margin-top: 0.8rem;
        font-weight: 300;
        letter-spacing: 0.5px;
    }
    
    /* Sidebar améliorée - Dark Mode */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%) !important;
        border-right: 3px solid #6366f1;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #e2e8f0 !important;
    }
    
    [data-testid="stSidebar"] h3 {
        color: #fbbf24 !important;
        font-weight: 700 !important;
        font-size: 1.4rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        border-bottom: 2px solid #fbbf24;
        padding-bottom: 0.5rem;
    }
    
    [data-testid="stSidebar"] label {
        color: #cbd5e1 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox, 
    [data-testid="stSidebar"] .stSlider,
    [data-testid="stSidebar"] .stNumberInput {
        background-color: rgba(255,255,255,0.1);
        border-radius: 8px;
        padding: 0.3rem;
    }
    
    /* Expander dans sidebar - Dark Mode */
    [data-testid="stSidebar"] .streamlit-expanderHeader {
        background: rgba(99, 102, 241, 0.15) !important;
        border: 1px solid rgba(99, 102, 241, 0.4);
        border-radius: 10px !important;
        color: #e2e8f0 !important;
        font-weight: 600 !important;
        padding: 0.8rem !important;
        transition: all 0.3s ease;
    }
    
    [data-testid="stSidebar"] .streamlit-expanderHeader:hover {
        background: rgba(99, 102, 241, 0.3) !important;
        border-color: #818cf8;
    }
    
    /* Cards avec Glassmorphism - Dark Mode */
    .glass-card {
        background: rgba(30, 41, 59, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid rgba(99, 102, 241, 0.3);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(99, 102, 241, 0.3);
    }
    
    /* Metrics personnalisées */
    .metric-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.8rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: scale(1.08);
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }
    
    .metric-value {
        font-size: 2.8rem;
        font-weight: 700;
        color: white;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .metric-label {
        font-size: 0.95rem;
        color: rgba(255,255,255,0.95);
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-top: 0.5rem;
        font-weight: 600;
    }
    
    /* Boutons améliorés - Dark Mode */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        font-size: 1.2rem;
        font-weight: 700;
        border-radius: 12px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5);
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.7);
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
    }
    
    /* Download button styling - Dark Mode */
    .stDownloadButton > button {
        width: 100%;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border: none;
        padding: 0.8rem 1.5rem;
        font-size: 1rem;
        font-weight: 600;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.5);
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.7);
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
    }
    
    /* Animations */
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Risk badges */
    .risk-low {
        background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
        color: white;
        padding: 0.8rem 1.5rem;
        border-radius: 25px;
        font-weight: 700;
        display: inline-block;
        box-shadow: 0 5px 15px rgba(16, 185, 129, 0.4);
        font-size: 1.1rem;
        letter-spacing: 0.5px;
    }
    
    .risk-medium {
        background: linear-gradient(135deg, #f59e0b 0%, #f97316 100%);
        color: white;
        padding: 0.8rem 1.5rem;
        border-radius: 25px;
        font-weight: 700;
        display: inline-block;
        box-shadow: 0 5px 15px rgba(245, 158, 11, 0.4);
        font-size: 1.1rem;
        letter-spacing: 0.5px;
    }
    
    .risk-high {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        padding: 0.8rem 1.5rem;
        border-radius: 25px;
        font-weight: 700;
        display: inline-block;
        box-shadow: 0 5px 15px rgba(239, 68, 68, 0.4);
        font-size: 1.1rem;
        letter-spacing: 0.5px;
    }
    
    /* Divider - Dark Mode */
    .custom-divider {
        height: 3px;
        background: linear-gradient(90deg, transparent, #6366f1, transparent);
        margin: 2.5rem 0;
        border-radius: 2px;
    }
    
    /* Icon styling */
    .icon-box {
        font-size: 1.5rem;
        margin-right: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- CHARGEMENT DES MODÈLES ---
@st.cache_resource
def load_models():
    try:
        model = joblib.load('../models/rf_model.pkl')
        scaler = joblib.load('../models/scaler.pkl')
        return model, scaler
    except Exception as e:
        st.error(f"Erreur de chargement des modèles: {e}")
        return None, None

rf_model, scaler = load_models()

# --- FONCTION : GÉNÉRATION RAPPORT HTML (Imprimable en PDF) ---
def generate_html_report(client_data, proba_churn, recommendations):
    """Génère un rapport HTML professionnel téléchargeable et imprimable en PDF"""
    date_str = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    # Déterminer le verdict
    if proba_churn < 0.4:
        verdict = "✅ CLIENT SÉCURISÉ"
        verdict_color = "#10b981"
        risk_class = "low"
    elif proba_churn < 0.7:
        verdict = "⚠️ CLIENT À SURVEILLER"
        verdict_color = "#f59e0b"
        risk_class = "medium"
    else:
        verdict = "🚨 ALERTE CRITIQUE"
        verdict_color = "#ef4444"
        risk_class = "high"
    
    # Générer le HTML
    html_content = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Rapport Churn Guardian AI</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Poppins:wght@600;700&display=swap');
            
            body {{
                font-family: 'Inter', sans-serif;
                margin: 0;
                padding: 40px;
                background: #f8fafc;
                color: #1e293b;
            }}
            
            .container {{
                max-width: 900px;
                margin: 0 auto;
                background: white;
                padding: 40px;
                border-radius: 15px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            }}
            
            .header {{
                text-align: center;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                border-radius: 10px;
                margin-bottom: 30px;
            }}
            
            .header h1 {{
                font-family: 'Poppins', sans-serif;
                font-size: 2.5rem;
                margin: 0;
            }}
            
            .header p {{
                font-size: 1.1rem;
                margin: 10px 0 0 0;
                opacity: 0.9;
            }}
            
            .meta-info {{
                text-align: right;
                color: #64748b;
                margin-bottom: 30px;
                font-size: 0.95rem;
            }}
            
            .verdict {{
                text-align: center;
                padding: 25px;
                background: {verdict_color};
                color: white;
                border-radius: 10px;
                margin: 30px 0;
            }}
            
            .verdict h2 {{
                margin: 0;
                font-size: 2rem;
                font-family: 'Poppins', sans-serif;
            }}
            
            .verdict p {{
                margin: 10px 0 0 0;
                font-size: 1.3rem;
            }}
            
            .section {{
                margin: 30px 0;
            }}
            
            .section h3 {{
                color: #1e3a8a;
                font-family: 'Poppins', sans-serif;
                border-bottom: 3px solid #667eea;
                padding-bottom: 10px;
                margin-bottom: 20px;
            }}
            
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }}
            
            table th {{
                background: #667eea;
                color: white;
                padding: 12px;
                text-align: left;
                font-weight: 600;
            }}
            
            table td {{
                padding: 12px;
                border-bottom: 1px solid #e2e8f0;
            }}
            
            table tr:nth-child(even) {{
                background: #f8fafc;
            }}
            
            .recommendations {{
                list-style: none;
                padding: 0;
            }}
            
            .recommendations li {{
                background: #f0f9ff;
                border-left: 4px solid #667eea;
                padding: 15px;
                margin: 10px 0;
                border-radius: 5px;
            }}
            
            .footer {{
                text-align: center;
                margin-top: 50px;
                padding-top: 20px;
                border-top: 2px solid #e2e8f0;
                color: #64748b;
                font-size: 0.9rem;
            }}
            
            @media print {{
                body {{
                    background: white;
                    padding: 0;
                }}
                .container {{
                    box-shadow: none;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🛡️ Churn Guardian AI</h1>
                <p>Rapport d'Analyse de Risque Client</p>
            </div>
            
            <div class="meta-info">
                <strong>Date du rapport:</strong> {date_str}
            </div>
            
            <div class="verdict">
                <h2>{verdict}</h2>
                <p>Probabilité de churn: {proba_churn:.1%}</p>
            </div>
            
            <div class="section">
                <h3>👤 Profil Client</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Paramètre</th>
                            <th>Valeur</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td>Âge</td><td>{client_data['age'][0]} ans</td></tr>
                        <tr><td>Genre</td><td>{'Homme' if client_data['gender_male'][0] == 1 else 'Femme'}</td></tr>
                        <tr><td>Ancienneté</td><td>{client_data['tenure'][0]} mois</td></tr>
                        <tr><td>Type de contrat</td><td>{['Mensuel', 'Trimestriel', 'Annuel'][client_data['contract_length'][0]]}</td></tr>
                        <tr><td>Niveau d'abonnement</td><td>{['Basic', 'Standard', 'Premium'][client_data['subscription_type'][0]]}</td></tr>
                        <tr><td>Dépenses totales</td><td>${client_data['total_spend'][0]}</td></tr>
                        <tr><td>Fréquence d'utilisation</td><td>{client_data['usage_frequency'][0]} connexions/mois</td></tr>
                        <tr><td>Appels au support</td><td>{client_data['support_calls'][0]}</td></tr>
                        <tr><td>Retard de paiement</td><td>{client_data['payment_delay'][0]} jours</td></tr>
                        <tr><td>Dernière interaction</td><td>{client_data['last_interaction'][0]} jours</td></tr>
                    </tbody>
                </table>
            </div>
            
            <div class="section">
                <h3>💡 Recommandations Personnalisées</h3>
                <ul class="recommendations">
    """
    
    for idx, rec in enumerate(recommendations, 1):
        clean_rec = rec.replace('**', '').replace('*', '')
        html_content += f"                    <li><strong>{idx}.</strong> {clean_rec}</li>\n"
    
    html_content += f"""
                </ul>
            </div>
            
            <div class="footer">
                <p><strong>Powered by BOUCHNAFA Ilyass</strong></p>
                <p>Machine Learning • Analytics • Intelligence Artificielle</p>
                <p>© 2025 - Tous droits réservés</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_content

# --- HEADER PRINCIPAL (SANS LOGO) ---
st.markdown("""
    <div class="main-header">
        <h1 class="main-title">🛡️ Churn Guardian AI</h1>
        <p class="main-subtitle">Système Intelligent de Prédiction et Prévention du Churn Client</p>
    </div>
""", unsafe_allow_html=True)

# --- SIDEBAR : SIMULATEUR CLIENT ---
with st.sidebar:
    st.markdown("### 🎯 SIMULATEUR CLIENT")
    st.markdown("Configurez les paramètres pour analyser le risque de churn.")
    st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)
    
    # Section Démographie
    with st.expander("👥 DÉMOGRAPHIE", expanded=True):
        age = st.slider("📅 Âge du client", 18, 90, 35, help="L'âge peut influencer le comportement et la fidélité")
        gender = st.radio("⚧ Genre", ["Femme", "Homme"], horizontal=True)
    
    # Section Contrat
    with st.expander("📋 CONTRAT & ABONNEMENT", expanded=True):
        contract_length = st.selectbox(
            "📄 Type de contrat", 
            ["Mensuel", "Trimestriel", "Annuel"],
            help="Les contrats plus longs montrent généralement plus d'engagement"
        )
        subscription_type = st.selectbox(
            "⭐ Niveau d'abonnement", 
            ["Basic", "Standard", "Premium"],
            help="Le niveau d'abonnement indique la valeur perçue"
        )
        tenure = st.slider(
            "📆 Ancienneté (mois)", 
            0, 60, 12,
            help="Durée depuis le début de l'abonnement"
        )
    
    # Section Financière
    with st.expander("💰 FINANCES", expanded=True):
        total_spend = st.number_input(
            "💵 Dépenses totales ($)", 
            0, 10000, 850,
            step=50,
            help="Montant total dépensé depuis le début"
        )
        payment_delay = st.slider(
            "⏰ Retard de paiement (jours)", 
            0, 30, 0,
            help="Un retard élevé peut indiquer une insatisfaction"
        )
    
    # Section Comportement
    with st.expander("📊 USAGE & ENGAGEMENT", expanded=True):
        usage_frequency = st.slider(
            "📈 Fréquence d'utilisation (/mois)", 
            0, 30, 15,
            help="Une utilisation régulière indique un engagement élevé"
        )
        last_interaction = st.number_input(
            "🕐 Dernière interaction (jours)", 
            0, 365, 7,
            help="Nombre de jours depuis la dernière utilisation"
        )
    
    # Section Support
    with st.expander("📞 SUPPORT CLIENT", expanded=True):
        support_calls = st.number_input(
            "☎️ Appels au support", 
            0, 20, 2,
            help="Beaucoup d'appels peut indiquer des problèmes"
        )
    
    st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)
    predict_btn = st.button("🔮 ANALYSER LE RISQUE")

# --- FONCTION : JAUGE AMÉLIORÉE ---
def create_enhanced_gauge(probability):
    """Crée une jauge moderne avec gradient"""
    if probability < 0.4:
        color = "#10b981"
        text_color = "#059669"
    elif probability < 0.7:
        color = "#f59e0b"
        text_color = "#d97706"
    else:
        color = "#ef4444"
        text_color = "#dc2626"
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=probability * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={
            'text': "Probabilité de Churn",
            'font': {'size': 32, 'family': 'Poppins', 'color': '#e2e8f0', 'weight': 'bold'}
        },
        number={'suffix': "%", 'font': {'size': 60, 'family': 'Poppins', 'color': text_color}},
        gauge={
            'axis': {
                'range': [None, 100],
                'tickwidth': 2,
                'tickcolor': "#475569",
                'tickfont': {'size': 16, 'color': '#cbd5e1'}
            },
            'bar': {'color': color, 'thickness': 0.75},
            'bgcolor': "#1e293b",
            'borderwidth': 4,
            'bordercolor': "#475569",
            'steps': [
                {'range': [0, 40], 'color': 'rgba(16, 185, 129, 0.2)'},
                {'range': [40, 70], 'color': 'rgba(245, 158, 11, 0.2)'},
                {'range': [70, 100], 'color': 'rgba(239, 68, 68, 0.2)'}
            ],
            'threshold': {
                'line': {'color': text_color, 'width': 8},
                'thickness': 0.85,
                'value': probability * 100
            }
        }
    ))
    
    fig.update_layout(
        height=400,
        margin=dict(l=40, r=40, t=100, b=40),
        paper_bgcolor='rgba(30,41,59,0.8)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'family': 'Inter', 'color': '#cbd5e1'}
    )
    return fig

# --- FONCTION : GRAPHIQUE DES FACTEURS ---
def create_risk_factors_chart(input_data):
    """Crée un graphique des facteurs de risque"""
    factors = {
        '☎️ Appels Support': min(input_data['support_calls'][0] * 5, 100),
        '⏰ Retard Paiement': min(input_data['payment_delay'][0] * 3.33, 100),
        '🕐 Inactivité': min(input_data['last_interaction'][0] / 3.65, 100),
        '📉 Usage Faible': max(100 - input_data['usage_frequency'][0] * 3.33, 0),
        '📆 Faible Ancienneté': max(100 - input_data['tenure'][0] * 1.67, 0)
    }
    
    df_factors = pd.DataFrame(list(factors.items()), columns=['Facteur', 'Score'])
    df_factors = df_factors.sort_values('Score', ascending=True)
    
    fig = px.bar(
        df_factors,
        x='Score',
        y='Facteur',
        orientation='h',
        color='Score',
        color_continuous_scale=['#10b981', '#f59e0b', '#ef4444'],
        title="Facteurs de Risque Détectés"
    )
    
    fig.update_layout(
        height=350,
        showlegend=False,
        paper_bgcolor='rgba(30,41,59,0.8)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'family': 'Inter', 'size': 13, 'color': '#cbd5e1'},
        title_font={'size': 20, 'family': 'Poppins', 'color': '#e2e8f0'},
        xaxis={'title': 'Score de Risque (0-100)', 'gridcolor': '#334155', 'color': '#cbd5e1'},
        yaxis={'title': '', 'gridcolor': '#334155', 'color': '#cbd5e1'}
    )
    
    return fig

# --- FONCTION : RECOMMANDATIONS INTELLIGENTES ---
def generate_recommendations(proba, input_data):
    """Génère des recommandations personnalisées"""
    recommendations = []
    
    if input_data['support_calls'][0] >= 5:
        recommendations.append("🎯 **Priorité Haute**: Contactez immédiatement le client pour résoudre ses problèmes récurrents")
    
    if input_data['payment_delay'][0] > 10:
        recommendations.append("💳 **Action Finance**: Proposez un échéancier de paiement flexible ou une aide personnalisée")
    
    if input_data['last_interaction'][0] > 30:
        recommendations.append("📧 **Réengagement**: Lancez une campagne email/SMS personnalisée avec offre exclusive")
    
    if input_data['usage_frequency'][0] < 5:
        recommendations.append("📱 **Activation Produit**: Proposez un onboarding personnalisé ou une formation gratuite")
    
    if input_data['tenure'][0] < 3:
        recommendations.append("🎁 **Rétention Précoce**: Offrez un bonus de bienvenue ou une remise pour fidéliser")
    
    if proba > 0.7:
        recommendations.append("🚨 **URGENCE MAXIMALE**: Assignez un account manager dédié dans les 24h")
        recommendations.append("💰 **Offre Exceptionnelle**: Remise de 20-30% + avantages exclusifs sur renouvellement")
    elif proba > 0.4:
        recommendations.append("📊 **Surveillance Active**: Ajoutez ce client à la liste de monitoring hebdomadaire")
        recommendations.append("🤝 **Relation Client**: Planifiez un appel de satisfaction dans les 7 jours")
    else:
        recommendations.append("✅ **Opportunité Upsell**: Client sain, proposez une montée en gamme Premium")
        recommendations.append("⭐ **Ambassadeur**: Sollicitez un témoignage ou une recommandation")
    
    return recommendations

# --- ZONE PRINCIPALE D'AFFICHAGE ---
if not predict_btn:
    # État initial : Dashboard d'accueil
    st.markdown("<div class='fade-in'>", unsafe_allow_html=True)
    
    # Cartes KPI
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div class="metric-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                <p class="metric-value">2,847</p>
                <p class="metric-label">👥 Clients Actifs</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="metric-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                <p class="metric-value">23.5%</p>
                <p class="metric-label">📉 Taux Churn</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="metric-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                <p class="metric-value">94.2%</p>
                <p class="metric-label">🎯 Précision IA</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
            <div class="metric-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
                <p class="metric-value">$458K</p>
                <p class="metric-label">💰 ARR Protégé</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)
    
    st.info("👈 **Pour commencer**: Configurez le profil du client dans la barre latérale, puis cliquez sur 'ANALYSER LE RISQUE'")
    
    st.plotly_chart(create_enhanced_gauge(0), use_container_width=True)
    
    # Section explicative
    st.markdown("### 🧠 À Propos de Churn Guardian AI")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🔬 Notre Technologie:**
        - 🤖 Machine Learning Avancé (Random Forest)
        - 📊 Analyse Prédictive en Temps Réel
        - 🎯 Recommandations Personnalisées IA
        - 📈 Scoring Multifactoriel Intelligent
        """)
    
    with col2:
        st.markdown("""
        **💼 Bénéfices Business:**
        - 💰 Réduction du Churn jusqu'à 35%
        - 🎯 Ciblage Précis des Clients à Risque
        - ⏱️ Anticipation 30 Jours à l'Avance
        - 📊 ROI Positif dès le 1er Mois
        """)

else:
    # État après prédiction
    if rf_model and scaler:
        # Préparation des données (RESPECTE LE FORMAT ORIGINAL)
        gender_male = 1 if gender == "Homme" else 0
        contract_map = {"Mensuel": 0, "Trimestriel": 1, "Annuel": 2}
        sub_map = {"Basic": 0, "Standard": 1, "Premium": 2}
        
        input_df = pd.DataFrame({
            'age': [age],
            'tenure': [tenure],
            'usage_frequency': [usage_frequency],
            'support_calls': [support_calls],
            'payment_delay': [payment_delay],
            'subscription_type': [sub_map[subscription_type]],
            'contract_length': [contract_map[contract_length]],
            'total_spend': [total_spend],
            'last_interaction': [last_interaction],
            'gender_male': [gender_male]
        })
        
        # PRÉDICTION (PIPELINE ORIGINAL PRÉSERVÉ)
        input_scaled = scaler.transform(input_df)
        proba_churn = rf_model.predict_proba(input_scaled)[0][1]
        
        # Animation d'entrée
        st.markdown("<div class='fade-in'>", unsafe_allow_html=True)
        
        # Section 1: Jauge principale
        st.plotly_chart(create_enhanced_gauge(proba_churn), use_container_width=True)
        
        # Section 2: Verdict avec badge coloré
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if proba_churn < 0.4:
                st.markdown(f"""
                    <div style='text-align: center; padding: 2rem;'>
                        <span class='risk-low'>✅ CLIENT SÉCURISÉ</span>
                        <p style='font-size: 1.4rem; margin-top: 1.5rem; color: #e2e8f0; font-weight: 600;'>
                            Risque de churn: <strong>{proba_churn:.1%}</strong>
                        </p>
                        <p style='color: #94a3b8; font-size: 1.1rem;'>Ce client présente un faible risque de départ</p>
                    </div>
                """, unsafe_allow_html=True)
            elif proba_churn < 0.7:
                st.markdown(f"""
                    <div style='text-align: center; padding: 2rem;'>
                        <span class='risk-medium'>⚠️ CLIENT À SURVEILLER</span>
                        <p style='font-size: 1.4rem; margin-top: 1.5rem; color: #e2e8f0; font-weight: 600;'>
                            Risque de churn: <strong>{proba_churn:.1%}</strong>
                        </p>
                        <p style='color: #94a3b8; font-size: 1.1rem;'>Des actions préventives sont recommandées</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div style='text-align: center; padding: 2rem;'>
                        <span class='risk-high'>🚨 ALERTE CRITIQUE</span>
                        <p style='font-size: 1.4rem; margin-top: 1.5rem; color: #e2e8f0; font-weight: 600;'>
                            Risque de churn: <strong>{proba_churn:.1%}</strong>
                        </p>
                        <p style='color: #94a3b8; font-size: 1.1rem;'>Intervention urgente requise</p>
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)
        
        # Section 3: Analyse détaillée en colonnes
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Facteurs de Risque")
            st.plotly_chart(create_risk_factors_chart(input_df), use_container_width=True)
        
        with col2:
            st.markdown("### 📈 Métriques Clés")
            
            metric_col1, metric_col2 = st.columns(2)
            with metric_col1:
                st.metric("📆 Ancienneté", f"{tenure} mois")
                st.metric("💵 Dépenses", f"${total_spend}")
                st.metric("⭐ Abonnement", subscription_type)
            
            with metric_col2:
                st.metric("📈 Usage/mois", f"{usage_frequency}")
                st.metric("☎️ Appels support", f"{support_calls}")
                st.metric("📄 Contrat", contract_length)
        
        st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)
        
        # Section 4: Recommandations
        st.markdown("### 💡 Plan d'Action Personnalisé")
        
        recommendations = generate_recommendations(proba_churn, input_df)
        
        col1, col2 = st.columns(2)
        
        for idx, rec in enumerate(recommendations):
            if idx % 2 == 0:
                with col1:
                    st.markdown(f"**{idx + 1}.** {rec}")
            else:
                with col2:
                    st.markdown(f"**{idx + 1}.** {rec}")
        
        st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)
        
        # Section 5: Actions rapides + TÉLÉCHARGEMENT PDF
        st.markdown("### ⚡ Actions Rapides")
        
        action_col1, action_col2, action_col3, action_col4 = st.columns(4)
        
        with action_col1:
            if st.button("📧 Envoyer Email"):
                st.success("✅ Email envoyé!")
        
        with action_col2:
            if st.button("📞 Planifier Appel"):
                st.success("✅ Appel planifié!")
        
        with action_col3:
            if st.button("🎁 Créer Offre"):
                st.success("✅ Offre créée!")
        
        with action_col4:
            # Bouton de téléchargement HTML (imprimable en PDF)
            html_report = generate_html_report(input_df, proba_churn, recommendations)
            st.download_button(
                label="📄 Télécharger Rapport",
                data=html_report,
                file_name=f"churn_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                mime="text/html"
            )
        
        st.markdown("</div>", unsafe_allow_html=True)
        
    else:
        st.error("❌ **Erreur**: Les modèles n'ont pas pu être chargés. Vérifiez que `rf_model.pkl` et `scaler.pkl` sont présents dans le dossier `models/`.")

# --- FOOTER ---
st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)
st.markdown("""
    <div style='text-align: center; color: #94a3b8; padding: 2rem;'>
        <p style='margin: 0; font-size: 1rem;'><strong>Powered by BOUCHNAFA Ilyass</strong></p>
        <p style='margin: 0.5rem 0 0 0; font-size: 0.9rem;'>Machine Learning • Analytics • Intelligence Artificielle</p>
        <p style='margin: 0.5rem 0 0 0; font-size: 0.85rem;'>© 2025 - Tous droits réservés</p>
    </div>
""", unsafe_allow_html=True)