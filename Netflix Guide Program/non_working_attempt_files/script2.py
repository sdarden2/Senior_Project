#New Scrape

#list of scripts
#React scripts
js_backend = "backend.js"
js_contentScript = "contentScript.js"
js_globalHook = "GlobalHook.js"

#custom script to grab movies
js_scrape = "scrape.js"
def inject_script(driver,script_name):
	script = open(script_name,'r').read()
	text = (r'var head = document.head;'
	'var script = document.createElement("script");'
	'script.type="text/javascript";'
	'script.text="' + script.replace("\n","") + '";'
	'head.appendChild(script);'
	)
	print text
	ret = driver.execute_script(text)
	return ret
	
def inject_react_scripts(driver):
	inject_script(driver,js_globalHook)
	inject_script(driver,js_backend)
	inject_script(driver,js_contentScript)
def get_movies_list(driver):
	script = open(js_scrape,'r').read()
	
	mlist = driver.execute_script(script)
	return mlist
	
def main():
	pass
	
if __name__ == "__main__":
	main()
