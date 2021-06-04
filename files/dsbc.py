from datetime import date

meses = {
    "Jan" : 1,
    "Fev" : 2,
    "Mar" : 3,
    "Abr" : 4,
    "Mai" : 5,
    "Jun" : 6,
    "Jul" : 7,
    "Ago" : 8,
    "Set" : 9,
    "Out" : 10,
    "Nov" : 11,
    "Dez" : 12
}

def para_dia(ano_mes, sep="/"):
  ano, mes = ano_mes.split(sep)
  return date(int(ano), meses[mes], 1)

def clean_n_join(df_dirty, df_ref):
	df_ref_c = df_ref.copy()
	df_dirty_c = df_dirty.copy()
	df_dirty_c = df_dirty_c[["Unidade federativa", "População"]]
	df_dirty_c.columns = ["uf", "populacao"]
	df_dirty_c = df_dirty_c.set_index("uf")
	df_dirty_c = df_dirty_c.dropna()
	df_dirty_c['populacao'] = df_dirty_c['populacao'].str.replace(" ","").astype(int)
	df_dirty_c.index = df_dirty_c.index.str.strip()
	# df_ref_c.index = df_ref_c.index.str[3:]
	for estado in df_ref_c.index:
		df_dirty_c.index = df_dirty_c.index.str.replace(f"{estado} {estado}", estado)
	return df_dirty_c.join(df_ref_c)

def gasos_e_gasto_por_habitante_para(todos_os_gastos, dados, mes: str):
	dados_c = dados.copy()
	todos_os_gastos_c = todos_os_gastos.copy()
	gastos_do_mes = todos_os_gastos_c[mes]
	gastos_do_mes.index = gastos_do_mes.index.str[3:]
	dados_c[f"gastos_{mes}"] = gastos_do_mes * 10**6
	dados_c[f"gastos_por_habitante_{mes}"] = dados_c[f"gastos_{mes}"] / dados_c["populacao"]
	return dados_c
