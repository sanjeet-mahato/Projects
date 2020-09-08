<?php
       session_start();
        if($_SESSION['selected']==6)
        {
            echo "
<html>
    <head>
        <link rel='stylesheet' type='text/css' href='admin_style.css'>
        <title>
           WELCOME TO ADMINISTRATOR UNIT
        </title>

    </head>

    
<body background='labo_back.jpg' > 
    <form action=lab_logic.php method='post'>
        <div id='head' style='float:left'>
            <h1 id='ha'>LABORATORIST UNIT</h1>
            
        </div>
        
         <div id='middle'  style='float:left'>
             <div id='middle_top' ></div>
             
            <input type = 'submit'  class='btn' value='Create Report' name='doctor' id='a'  style='background-image: url(report.png);image-orientation: center;position:absolute;left:310px;top:150px;'/><br/><br/>
             <input type = 'submit'  class='btn' value = 'Create Invoice' name='patient'  id='b'  style='background-image: url(inv.png);image-orientation: center;position:absolute;left:100px;top:400px;'/><br/><br/>
            
            
             <input type = 'submit' class='btn' value = 'Salary History' name='account'   id='f'  style='background-image: url(account.png);image-orientation: center;position:absolute;left:500px;top:400px;'/><br/><br/>
            
             <input type = 'submit' class='btn2' value = 'LOG_OUT' name='log_out'   id='g'  style='background-image: url(logout.png);image-orientation: center;position:absolute;left:1150px;top:40px;'  /><br/><br/>
                
             <input type = 'submit' class='btn2' value = 'MY_PROFILE' name='info'   id='h'  style='height:70px;width:70px;background-image: url(profile.png);image-orientation: center;position:absolute;left:70px;top:20px;'  /><br/><br/>
            
             
        </div>
        
        
    
    </form>
    
    </body>
</html>
";

        }
        else
        {
             header("refresh:1 url=login_new.html");
        }
    
?>