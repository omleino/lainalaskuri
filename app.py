import streamlit as st
import pandas as pd

st.set_page_config(page_title="Taloyhtiön lainalaskuri", layout="centered")
st.title("🏢 Taloyhtiön lainalaskuri – tasalyhenteinen laina")

# Käyttäjän syötteet
neliot = st.number_input("Maksavat neliöt (m²)", min_value=1, value=1000)
investointi = st.number_input("Investoinnin suuruus (€)", min_value=0.0, value=500000.0, step=10000.0)
korko_prosentti = st.number_input("Korko (%)", min_value=0.0, value=4.0, step=0.1, format="%.1f")
vuodet = st.number_input("Takaisinmaksuaika (vuotta)", min_value=1, max_value=25, value=20)

# Laskenta
korko = korko_prosentti / 100
lainamaara_per_nelio = investointi / neliot
vuosittainen_lyhennys = investointi / vuodet
jalkijelkeinen_laina = investointi

data = []

for vuosi in range(1, 26):
    if vuosi <= vuodet:
        korko_vuodelle = jalkijelkeinen_laina * korko
        paoma_per_nelio = vuosittainen_lyhennys / neliot
        korko_per_nelio = korko_vuodelle / neliot
        kuukausi_vastike = (paoma_per_nelio + korko_per_nelio) / 12
        jalkijelkeinen_laina -= vuosittainen_lyhennys
    else:
        paoma_per_nelio = 0
        korko_per_nelio = 0
        kuukausi_vastike = 0

    data.append({
        "Vuosi": vuosi,
        "Pääoma €/m²/vuosi": round(paoma_per_nelio, 2),
        "Korko €/m²/vuosi": round(korko_per_nelio, 2),
        "Vastike €/m²/kk": round(kuukausi_vastike, 2)
    })

df = pd.DataFrame(data)
kokonaiskustannus_per_nelio = df["Pääoma €/m²/vuosi"].sum() + df["Korko €/m²/vuosi"].sum()

# Näyttö
st.subheader("📊 Yhteenveto")
st.markdown(f"**Investointi per m²:** {lainamaara_per_nelio:.2f} €")
st.markdown(f"**Kokonaiskustannus per m² (sis. korot):** {kokonaiskustannus_per_nelio:.2f} €")

st.subheader("📅 Vuosittaiset vastikkeet per m²")
st.dataframe(df.style.format({
    "Pääoma €/m²/vuosi": "{:.2f}",
    "Korko €/m²/vuosi": "{:.2f}",
    "Vastike €/m²/kk": "{:.2f}"
}), use_container_width=True)
