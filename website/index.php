<html>
    <head>
        <title>CIS 322 REST-api demo: Laptop list</title>
    </head>

    <body>
        
        <h1>List of Open Times (defaults to JSON)</h1>
        <ul>
            <?php
            $json = file_get_contents('http://api-service/listOpenOnly');
            $obj = json_decode($json);
	          $opens = $obj->result;
            foreach ($opens as $openTime) {
                echo "<li>$openTime</li>";
            }
            ?>
        </ul>

        <h1>List of Open Times (JSON)</h1>
        <ul>
            <?php
            $json = file_get_contents('http://api-service/listOpenOnly/json');
            $obj = json_decode($json);
	          $opens = $obj->result;
            foreach ($opens as $openTime) {
                echo "<li>$openTime</li>";
            }
            ?>
        </ul>

        <h1>List of Close Times (JSON)</h1>
        <ul>
            <?php
            $json = file_get_contents('http://api-service/listCloseOnly/json');
            $obj = json_decode($json);
	          $opens = $obj->result;
            foreach ($opens as $openTime) {
                echo "<li>$openTime</li>";
            }
            ?>
        </ul>

	<h1>List of All Times (JSON)</h1>
        <ul>
            <?php
            $json = file_get_contents('http://api-service/listAll/json');
            $obj = json_decode($json);
	          $opens = $obj->result;
            foreach ($opens as $timeEntry) {
                 echo "<li>$timeEntry</li>";
            }
            ?>
        </ul>

	<h1>List of Open Times (csv)</h1>
        <ul>
            <?php
            $json = file_get_contents('http://api-service/listOpenOnly/csv');
            $obj = json_decode($json);
                  echo "<li>$obj</li>";
            ?>
        </ul>

	<h1>List of Close Times (csv)</h1>
        <ul>
            <?php
            $json = file_get_contents('http://api-service/listCloseOnly/csv');
            $obj = json_decode($json);
                  echo "<li>$obj</li>";
            ?>
        </ul>

	<h1>List of All Times (csv)</h1>
        <ul>
            <?php
            $json = file_get_contents('http://api-service/listAll/csv');
            $obj = json_decode($json);
                  echo "<li>$obj</li>";
            ?>
        </ul>

	<h1>List of All Times (csv) with Top = 3</h1>
        <ul>
            <?php
            $json = file_get_contents('http://api-service/listAll/csv?top=3');
            $obj = json_decode($json);
                  echo "<li>$obj</li>";
            ?>
        </ul>

	<h1>List of All Times (JSON) with Top = 5</h1>
        <ul>
            <?php
            $json = file_get_contents('http://api-service/listAll/json?top=5');
            $obj = json_decode($json);
	          $opens = $obj->result;
            foreach ($opens as $timeEntry) {
                 echo "<li>$timeEntry</li>";
            }
            ?>
        </ul>


    </body>
</html>

