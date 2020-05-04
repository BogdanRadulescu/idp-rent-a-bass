<h1>Rent-a-Bass</h1>
<h4>Rădulescu Bogdan Alexandru - 341C3</h4>

<ol style="font-weight: bold;">
	<li>
Serviciul <b><i>admin</b></i> poate fi accesat la 		<i>localhost:8009</i> cu <b>username</b> <i>admin</i> și <b>password</b> <i>admin</i> și permite adăugarea de <i>useri</i> și <i>instrumente</i>
	</li>
	<br>
	<li>
Serviciul <b><i>server</b></i> poate fi accesat la 		<i>localhost:8000</i> și permite navigarea prin diverse meniuri, închirierea de instrumente muzicale, precum și vizionarea de statistici și bilanțuri personale
	</li>
		<br>
	<li>
Serviciul <b><i>database</b></i> poate fi accesat cu <br>&emsp;&emsp;<i>mysql -h 127.0.0.1 -u root -p</i><br> și permite conexiunea în CLI la baza de date. În ea sunt stocate datele și procedurile utilizate de aplicație
	</li>
	<br>
	<li>
Serviciul <b><i>visualizer</b></i> poate fi accesat la 		<i>localhost:3000</i> cu <b>username</b> <i>admin</i> și <b>password</b> <i>admin</i> și permite vizualizarea prin <i>Grafana</i> a statisticilor despre aplicație
	</li>
	<br>
	<li>
Serviciul <b><i>bank</b></i> nu ar trebui accesat direct. Este folosit drept interfata pentru tranzactii secure.
	</li>
</ol>

Pentru a opri toate containerele:
&emsp;<i>docker stop $(docker ps -a -q)</i>
Pentru a șterge toate containerele:
&emsp;<i>docker rm $(docker ps -a -q)</i>
