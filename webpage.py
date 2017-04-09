from flask import Flask, request
app = Flask(__name__)

@app.route("/")
def set_switch():
		SW = request.args.get("SW")
		msg = request.args.get("msg")
		if(SW == "1"):
			SWfile = open("./SW1msg", 'w')
		elif(SW =="2"):
			SWfile = open("./SW2msg", 'w')
		elif (SW == "3"):
			SWfile = open("./SW3msg", 'w')
		else:
			return "<html> <head> <title> WebPage </title> <script> function changemsg1() { document.location = \"/?SW=1&msg=\" + document.getElementById(\"msg\").value } function changemsg2() { document.location = \"/?SW=2&msg=\" + document.getElementById(\"msg\").value } function changemsg3() { document.location = \"/?SW=3&msg=\" + document.getElementById(\"msg\").value } </script> </head> <body> <input type=\"text\" id=\"msg\" > <button type=\"button\" onclick=\"changemsg1()\"> SW1 change </button> <button type=\"button\" onclick=\"changemsg2()\"> SW2 change </button> <button type=\"button\" onclick=\"changemsg3()\"> SW3 change </button> </body> </html>"
		SWfile.write(msg)
		SWfile.close()
		return "<html> <head> <script> function startup() { document.location = \"/\" } </script> </head> <body> Success! </body> </html>"

if __name__ == "__main__":
	app.run(debug=True, host="10.42.0.90")		

