import pandas as pd
import requests
import urllib.parse

df = pd.read_excel("productos.xlsx")

headers = {"User-Agent": "Mozilla/5.0"}

# --- función para calcular descuento ---
def calc_desc(price, list_price):
    if list_price and list_price > price:
        return round((list_price - price) / list_price * 100, 2)
    return 0


# --- FARMACITY ---
def farmacity_data(desc):
    q = urllib.parse.quote(desc)
    url = f"https://www.farmacity.com/api/catalog_system/pub/products/search?ft={q}"
    r = requests.get(url, headers=headers)

    if r.status_code == 200 and r.text.strip():
        data = r.json()
        if data:
            try:
                prod = data[0]
                offer = prod["items"][0]["sellers"][0]["commertialOffer"]

                price = offer["Price"]
                list_price = offer.get("ListPrice", price)
                desc_pct = calc_desc(price, list_price)

                link = f"https://www.farmacity.com/{prod['linkText']}/p"
                return price, list_price, desc_pct, link
            except:
                pass
    return None, None, None, None


# --- FARMAPLUS ---
def farmaplus_data(desc):
    q = urllib.parse.quote(desc)
    url = f"https://www.farmaplus.com.ar/api/catalog_system/pub/products/search?ft={q}"
    r = requests.get(url, headers=headers)

    if r.status_code == 200 and r.text.strip():
        data = r.json()
        if data:
            try:
                prod = data[0]
                offer = prod["items"][0]["sellers"][0]["commertialOffer"]

                price = offer["Price"]
                list_price = offer.get("ListPrice", price)
                desc_pct = calc_desc(price, list_price)

                link = f"https://www.farmaplus.com.ar/{prod['linkText']}/p"
                return price, list_price, desc_pct, link
            except:
                pass
    return None, None, None, None


# --- listas resultado ---
fc_price, fc_list, fc_desc, fc_link = [], [], [], []
fp_price, fp_list, fp_desc, fp_link = [], [], [], []

for _, row in df.iterrows():
    desc = str(row["descripcion"])

    p1, lp1, d1, l1 = farmacity_data(desc)
    p2, lp2, d2, l2 = farmaplus_data(desc)

    fc_price.append(p1)
    fc_list.append(lp1)
    fc_desc.append(d1)
    fc_link.append(l1)

    fp_price.append(p2)
    fp_list.append(lp2)
    fp_desc.append(d2)
    fp_link.append(l2)


df["precio_farmacity"] = fc_price
df["precio_lista_farmacity"] = fc_list
df["descuento_farmacity_%"] = fc_desc
df["link_farmacity"] = fc_link

df["precio_farmaplus"] = fp_price
df["precio_lista_farmaplus"] = fp_list
df["descuento_farmaplus_%"] = fp_desc
df["link_farmaplus"] = fp_link

df.to_excel("comparador_precios.xlsx", index=False)

print("comparador con descuentos listo 😎")
