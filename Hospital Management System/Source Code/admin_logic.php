<?php
$link=mysqli_connect("localhost","root","","hosp");
    if($link==false)
    {
        die("ERROR ".mysqli_connect_error());
    }
    if($_SERVER["REQUEST_METHOD"]=="POST"){
        
        session_start();
        if(isset($_POST['doctor']))
        {   
            $sql="SELECT * FROM profile";
         $mydata=mysqli_query($link,$sql);
            echo "<form action=edit_pro.php method=post>";
           echo "<body style='margin: 0em auto;background-color:#E0FFFF'><div style='height:15px;width:1400px;background-color:teal;'></div><div style='height:100px;width:1400px;background-color:teal;text-align:center;float:left'><h1 style='color:white;font-size:35px'>DOCTORS LIST</h1></div><div style='height:40px;width:1400px;float:left;background-color:#E0FFFF'></div><div style='height:700px;width:515px;float:left'></div><div style='position:absolute;left:90px;top:150px;float:center'>";
            echo "<table text-align=center border=1 style='background-color:#F5FFFA;font-size:14px'>
                <tr style='color:red;font-weight:bold'>
                   <td style='text-align:center'> User Id</td>
                    <td style='text-align:center'> Name</td>
                     <td style='text-align:center'> Department</td>
                     <td style='text-align:center'> Sex</td>
                    <td style='text-align:center'> Age</td>
                    <td style='text-align:center'> Blood Group</td>
                    <td style='text-align:center'> Email</td>
                    <td style='text-align:center'> Phone</td>
                    <td style='text-align:center'> Address</td>
                    <td style='text-align:center'> Update</td>
                    <td style='text-align:center'> Delete</td>
                </tr>";
            $count=0;
            $name_ch="name$count";
            $sex_ch="sex$count";
            $age_ch="age$count";
            $blood_ch="blood$count";
            $em_ch="em$count";
            $tel_ch="tel$count";
            $add_ch="add$count";
            $user_ch="user$count";
            $type_ch="type$count";
            $pass_ch="pass$count";
            $dep_ch="dep$count";
            $up_ch="up$count";
            $del_ch="del$count";
            
         while($record=mysqli_fetch_array($mydata))
         {
             //echo $record['Product']."<br/>";
             $name=$record['Name'];
             $sex=$record['Sex'];
             $age=$record['Age'];
             $blood=$record['Blood_Group'];
             $em=$record['Email_Id'];
             $tel=$record['Telephone_No'];
             $add=$record['Address'];
             $user=$record['User_Id'];
             $type=$record['User_Type'];
             $pass=$record['Password'];
             $dep=$record['Department'];
             if($type=='Doctor')
             echo "<tr><td  style='text-align:center' name=$user_ch value=$user size='10'>$user</td><td><input type=text style='text-align:center'  name=$name_ch value='$name' size='10'></td><td><input type=text style='text-align:center'  name=$dep_ch value='$dep' size='10'></td><td><input type=text style='text-align:center'  name=$sex_ch value=$sex size='6'></td><td><input type=text style='text-align:center'  name=$age_ch value=$age size='3'></td><td><input type=text style='text-align:center'  name=$blood_ch value=$blood size='5'></td><td><input type=text style='text-align:center'  name=$em_ch value=$em size='15'></td><td><input type=text style='text-align:center'  name=$tel_ch value=$tel size='12'></td><td><input type=text style='text-align:center'  name=$add_ch value='$add' size='20'></td><td><input type=submit name=$up_ch value=Update style='background-color:green;font-size:18px;color:white'></td><td><input type=submit name=$del_ch value=Remove style='background-color:red;font-size:18px;color:white'></td></tr>";
             $count=$count+1;
             $name_ch="name$count";
            $sex_ch="sex$count";
            $age_ch="age$count";
            $blood_ch="blood$count";
             $em_ch="em$count";
            $tel_ch="tel$count";
            $add_ch="add$count";
            $user_ch="user$count";
            $type_ch="type$count";
            $pass_ch="pass$count";
            $dep_ch="dep$count";
            $up_ch="up$count";
            $del_ch="del$count";
         }
             echo "</table>";
             echo "<input type=submit value='Add Doctor' name='add_pr' style='background-color:blue;font-size:18px;color:white'/>";
                     echo "</div></body></form>"; 
         
        }
        elseif(isset($_POST['patient']))
        {   
            $sql="SELECT * FROM profile";
         $mydata=mysqli_query($link,$sql);
            echo "<form action=edit_pro.php method=post>";
           echo "<body style='margin: 0em auto;background-color:#E0FFFF'><div style='height:15px;width:1400px;background-color:teal;'></div><div style='height:100px;width:1400px;background-color:teal;text-align:center;float:left'><h1 style='color:white;font-size:35px'>PATIENTS LIST</h1></div><div style='height:40px;width:1400px;float:left;background-color:#E0FFFF'></div><div style='height:700px;width:515px;float:left'></div><div style='position:absolute;left:60px;top:150px;float:center'>";
            echo "<table text-align=center border=1 style='background-color:#F5FFFA;font-size:14px'>
                <tr style='color:red;font-weight:bold'>
                   <td style='text-align:center'> User Id</td>
                    <td style='text-align:center'> Name</td>
                    <td style='text-align:center'> Supervising Doctor</td>
                     <td style='text-align:center'> Sex</td>
                    <td style='text-align:center'> Age</td>
                    <td style='text-align:center'> Blood Group</td>
                   <td style='text-align:center'> Email</td>
                    <td style='text-align:center'> Phone</td>
                    <td style='text-align:center'> Address</td>
                    <td style='text-align:center'> Update</td>
                    <td style='text-align:center'> Delete</td>
                </tr>";
            $count=0;
            $name_ch="name$count";
            $sex_ch="sex$count";
            $age_ch="age$count";
            $blood_ch="blood$count";
            $em_ch="em$count";
            $tel_ch="tel$count";
            $add_ch="add$count";
            $user_ch="user$count";
            $type_ch="type$count";
            $pass_ch="pass$count";
            $dep_ch="dep$count";
            $up_ch="up$count";
            $del_ch="del$count";
            
         while($record=mysqli_fetch_array($mydata))
         {
             //echo $record['Product']."<br/>";
             $name=$record['Name'];
             $sex=$record['Sex'];
             $age=$record['Age'];
             $blood=$record['Blood_Group'];
             $em=$record['Email_Id'];
             $tel=$record['Telephone_No'];
             $add=$record['Address'];
             $user=$record['User_Id'];
             $type=$record['User_Type'];
             $pass=$record['Password'];
             $dep=$record['Department'];
             if($type=='Patient')
             echo "<tr><td  style='text-align:center' name=$user_ch value=$user size='10'>$user</td><td><input type=text style='text-align:center'  name=$name_ch value='$name' size='15'><td><input type=text style='text-align:center'  name=$dep_ch value='$dep' size='15'></td><td><input type=text style='text-align:center'  name=$sex_ch value=$sex size='6'></td><td><input type=text style='text-align:center'  name=$age_ch value=$age size='3'></td><td><input type=text style='text-align:center'  name=$blood_ch value=$blood size='5'></td><td><input type=text style='text-align:center'  name=$em_ch value=$em size='15'></td><td><input type=text style='text-align:center'  name=$tel_ch value=$tel size='12'></td><td><input type=text style='text-align:center'  name=$add_ch value='$add' size='20'></td><td><input type=submit name=$up_ch value=Update style='background-color:green;font-size:18px;color:white'></td><td><input type=submit name=$del_ch value=Remove style='background-color:red;font-size:18px;color:white'></td></tr>";
             $count=$count+1;
             $name_ch="name$count";
            $sex_ch="sex$count";
            $age_ch="age$count";
            $blood_ch="blood$count";
            $em_ch="em$count";
            $tel_ch="tel$count";
            $add_ch="add$count";
            $user_ch="user$count";
            $type_ch="type$count";
            $pass_ch="pass$count";
            $dep_ch="dep$count";
            $up_ch="up$count";
            $del_ch="del$count";
         }
             echo "</table>";
             echo "<input type=submit value='Add Patient' name='add_pt' style='background-color:blue;font-size:18px;color:white'/>";
                     echo "</div></body></form>"; 
         
        }
        elseif(isset($_POST['nurse']))
        {   
            $sql="SELECT * FROM profile";
         $mydata=mysqli_query($link,$sql);
            echo "<form action=edit_pro.php method=post>";
           echo "<body style='margin: 0em auto;background-color:#E0FFFF'><div style='height:15px;width:1400px;background-color:teal;'></div><div style='height:100px;width:1400px;background-color:teal;text-align:center;float:left'><h1 style='color:white;font-size:35px'>NURSES LIST</h1></div><div style='height:40px;width:1400px;float:left;background-color:#E0FFFF'></div><div style='height:700px;width:515px;float:left'></div><div style='position:absolute;left:70px;top:150px;float:center'>";
            echo "<table text-align=center border=1 style='background-color:#F5FFFA;font-size:14px'>
                <tr style='color:red;font-weight:bold'>
                   <td style='text-align:center'> User Id</td>
                    <td style='text-align:center'> Name</td>
                     <td style='text-align:center'> Department</td>
                    <td style='text-align:center'> Sex</td>
                    <td style='text-align:center'> Age</td>
                    <td style='text-align:center'> Blood Group</td>
                   <td style='text-align:center'> Email</td>
                    <td style='text-align:center'> Phone</td>
                    <td style='text-align:center'> Address</td>
                    <td style='text-align:center'> Update</td>
                    <td style='text-align:center'> Delete</td>
                </tr>";
            $count=0;
            $name_ch="name$count";
            $sex_ch="sex$count";
            $age_ch="age$count";
            $blood_ch="blood$count";
            $em_ch="em$count";
            $tel_ch="tel$count";
            $add_ch="add$count";
            $user_ch="user$count";
            $type_ch="type$count";
            $pass_ch="pass$count";
            $dep_ch="dep$count";
            $up_ch="up$count";
            $del_ch="del$count";
            
         while($record=mysqli_fetch_array($mydata))
         {
             //echo $record['Product']."<br/>";
             $name=$record['Name'];
             $sex=$record['Sex'];
             $age=$record['Age'];
             $blood=$record['Blood_Group'];
             $em=$record['Email_Id'];
             $tel=$record['Telephone_No'];
             $add=$record['Address'];
             $user=$record['User_Id'];
             $type=$record['User_Type'];
             $pass=$record['Password'];
             $dep=$record['Department'];
             if($type=='Nurse')
             echo "<tr><td  style='text-align:center' name=$user_ch value=$user size='10'>$user</td><td><input type=text style='text-align:center'  name=$name_ch value='$name' size='15'></td><td><input type=text style='text-align:center'  name=$dep_ch value='$dep' size='15'></td><td><input type=text style='text-align:center'  name=$sex_ch value=$sex size='6'></td><td><input type=text style='text-align:center'  name=$age_ch value=$age size='3'></td><td><input type=text style='text-align:center'  name=$blood_ch value=$blood size='5'></td><td><input type=text style='text-align:center'  name=$em_ch value=$em size='15'></td><td><input type=text style='text-align:center'  name=$tel_ch value=$tel size='12'></td><td><input type=text style='text-align:center'  name=$add_ch value='$add' size='20'></td><td><input type=submit name=$up_ch value=Update style='background-color:green;font-size:18px;color:white'></td><td><input type=submit name=$del_ch value=Remove style='background-color:red;font-size:18px;color:white'></td></tr>";
             $count=$count+1;
             $name_ch="name$count";
            $sex_ch="sex$count";
            $age_ch="age$count";
            $blood_ch="blood$count";
            $em_ch="em$count";
            $tel_ch="tel$count";
            $add_ch="add$count";
            $user_ch="user$count";
            $type_ch="type$count";
            $pass_ch="pass$count";
            $dep_ch="dep$count";
            $up_ch="up$count";
            $del_ch="del$count";
         }
             echo "</table>";
             echo "<input type=submit value='Add Nurse' name='add_nr' style='background-color:blue;font-size:18px;color:white'/>";
                     echo "</div></body></form>"; 
         
        }
        elseif(isset($_POST['pharmacy']))
        {   
            $sql="SELECT * FROM profile";
         $mydata=mysqli_query($link,$sql);
            echo "<form action=edit_pro.php method=post>";
           echo "<body style='margin: 0em auto;background-color:#E0FFFF'><div style='height:15px;width:1400px;background-color:teal;'></div><div style='height:100px;width:1400px;background-color:teal;text-align:center;float:left'><h1 style='color:white;font-size:35px'>PHARMACISTS LIST</h1></div><div style='height:40px;width:1400px;float:left;background-color:#E0FFFF'></div><div style='height:700px;width:515px;float:left'></div><div style='position:absolute;left:110px;top:150px;float:center'>";
            echo "<table text-align=center border=1 style='background-color:#F5FFFA;font-size:14px'>
                <tr style='color:red;font-weight:bold'>
                   <td style='text-align:center'> User Id</td>
                    <td style='text-align:center'> Name</td>
                     <td style='text-align:center'> Sex</td>
                    <td style='text-align:center'> Age</td>
                    <td style='text-align:center'> Blood Group</td>
                   <td style='text-align:center'> Email</td>
                    <td style='text-align:center'> Phone</td>
                    <td style='text-align:center'> Address</td>
                    <td style='text-align:center'> Update</td>
                    <td style='text-align:center'> Delete</td>
                </tr>";
            $count=0;
            $name_ch="name$count";
            $sex_ch="sex$count";
            $age_ch="age$count";
            $blood_ch="blood$count";
            $em_ch="em$count";
            $tel_ch="tel$count";
            $add_ch="add$count";
            $user_ch="user$count";
            $type_ch="type$count";
            $pass_ch="pass$count";
            $dep_ch="dep$count";
            $up_ch="up$count";
            $del_ch="del$count";
            
         while($record=mysqli_fetch_array($mydata))
         {
             //echo $record['Product']."<br/>";
             $name=$record['Name'];
             $sex=$record['Sex'];
             $age=$record['Age'];
             $blood=$record['Blood_Group'];
             $em=$record['Email_Id'];
             $tel=$record['Telephone_No'];
             $add=$record['Address'];
             $user=$record['User_Id'];
             $type=$record['User_Type'];
             $pass=$record['Password'];
             $dep=$record['Department'];
             if($type=='Pharmacist')
             echo "<tr><td  style='text-align:center' name=$user_ch value=$user size='10'>$user</td><td><input type=text style='text-align:center'  name=$name_ch value='$name' size='15'></td><td><input type=text style='text-align:center'  name=$sex_ch value=$sex size='6'></td><td><input type=text style='text-align:center'  name=$age_ch value=$age size='3'></td><td><input type=text style='text-align:center'  name=$blood_ch value=$blood size='5'></td><td><input type=text style='text-align:center'  name=$em_ch value=$em size='15'></td><td><input type=text style='text-align:center'  name=$tel_ch value=$tel size='12'></td><td><input type=text style='text-align:center'  name=$add_ch value='$add' size='20'></td><td><input type=submit name=$up_ch value=Update style='background-color:green;font-size:18px;color:white'></td><td><input type=submit name=$del_ch value=Remove style='background-color:red;font-size:18px;color:white'></td></tr>";
             $count=$count+1;
             $name_ch="name$count";
            $sex_ch="sex$count";
            $age_ch="age$count";
            $blood_ch="blood$count";
            $em_ch="em$count";
            $tel_ch="tel$count";
            $add_ch="add$count";
            $user_ch="user$count";
            $type_ch="type$count";
            $pass_ch="pass$count";
            $dep_ch="dep$count";
            $up_ch="up$count";
            $del_ch="del$count";
         }
             echo "</table>";
             echo "<input type=submit value='Add Pharmacist' name='add_ph' style='background-color:blue;font-size:18px;color:white'/>";
                     echo "</div></body></form>"; 
         
        }
        elseif(isset($_POST['labo']))
        {   
            $sql="SELECT * FROM profile";
         $mydata=mysqli_query($link,$sql);
            echo "<form action=edit_pro.php method=post>";
           echo "<body style='margin: 0em auto;background-color:#E0FFFF'><div style='height:15px;width:1400px;background-color:teal;'></div><div style='height:100px;width:1400px;background-color:teal;text-align:center;float:left'><h1 style='color:white;font-size:35px'>LABORATORISTS LIST</h1></div><div style='height:40px;width:1400px;float:left;background-color:#E0FFFF'></div><div style='height:700px;width:515px;float:left'></div><div style='position:absolute;left:150px;top:150px;float:center'>";
            echo "<table text-align=center border=1 style='background-color:#F5FFFA;font-size:14px'>
                <tr style='color:red;font-weight:bold'>
                   <td style='text-align:center'> User Id</td>
                    <td style='text-align:center'> Name</td>
                     <td style='text-align:center'> Sex</td>
                    <td style='text-align:center'> Age</td>
                    <td style='text-align:center'> Blood Group</td>
                   <td style='text-align:center'> Email</td>
                    <td style='text-align:center'> Phone</td>
                    <td style='text-align:center'> Address</td>
                    <td style='text-align:center'> Update</td>
                    <td style='text-align:center'> Delete</td>
                </tr>";
            $count=0;
            $name_ch="name$count";
            $sex_ch="sex$count";
            $age_ch="age$count";
            $blood_ch="blood$count";
            $em_ch="em$count";
            $tel_ch="tel$count";
            $add_ch="add$count";
            $user_ch="user$count";
            $type_ch="type$count";
            $pass_ch="pass$count";
            $dep_ch="dep$count";
            $up_ch="up$count";
            $del_ch="del$count";
            
         while($record=mysqli_fetch_array($mydata))
         {
             //echo $record['Product']."<br/>";
             $name=$record['Name'];
             $sex=$record['Sex'];
             $age=$record['Age'];
             $blood=$record['Blood_Group'];
             $em=$record['Email_Id'];
             $tel=$record['Telephone_No'];
             $add=$record['Address'];
             $user=$record['User_Id'];
             $type=$record['User_Type'];
             $pass=$record['Password'];
             $dep=$record['Department'];
             if($type=='Laboratorist')
             echo "<tr><td  style='text-align:center' name=$user_ch value=$user size='10'>$user</td><td><input type=text style='text-align:center'  name=$name_ch value='$name' size='15'></td><td><input type=text style='text-align:center'  name=$sex_ch value=$sex size='6'></td><td><input type=text style='text-align:center'  name=$age_ch value=$age size='3'></td><td><input type=text style='text-align:center'  name=$blood_ch value=$blood size='5'></td><td><input type=text style='text-align:center'  name=$em_ch value=$em size='15'></td><td><input type=text style='text-align:center'  name=$tel_ch value=$tel size='12'></td><td><input type=text style='text-align:center'  name=$add_ch value='$add' size='20'></td><td><input type=submit name=$up_ch value=Update style='background-color:green;font-size:18px;color:white'></td><td><input type=submit name=$del_ch value=Remove style='background-color:red;font-size:18px;color:white'></td></tr>";
             $count=$count+1;
             $name_ch="name$count";
            $sex_ch="sex$count";
            $age_ch="age$count";
            $blood_ch="blood$count";
            $em_ch="em$count";
            $tel_ch="tel$count";
            $add_ch="add$count";
            $user_ch="user$count";
            $type_ch="type$count";
            $pass_ch="pass$count";
            $dep_ch="dep$count";
            $up_ch="up$count";
            $del_ch="del$count";
         }
             echo "</table>";
             echo "<input type=submit value='Add Laboratorist' name='add_lb' style='background-color:blue;font-size:18px;color:white'/>";
                     echo "</div></body></form>"; 
         
        }
        elseif(isset($_POST['account']))
        {   
            $sql="SELECT * FROM profile";
         $mydata=mysqli_query($link,$sql);
            echo "<form action=edit_pro.php method=post>";
           echo "<body style='margin: 0em auto;background-color:#E0FFFF'><div style='height:15px;width:1400px;background-color:teal;'></div><div style='height:100px;width:1400px;background-color:teal;text-align:center;float:left'><h1 style='color:white;font-size:35px'>ACCOUNTANTS LIST</h1></div><div style='height:40px;width:1400px;float:left;background-color:#E0FFFF'></div><div style='height:700px;width:515px;float:left'></div><div style='position:absolute;left:150px;top:150px;float:center'>";
            echo "<table text-align=center border=1 style='background-color:#F5FFFA;font-size:14px'>
                <tr style='color:red;font-weight:bold'>
                   <td style='text-align:center'> User Id</td>
                    <td style='text-align:center'> Name</td>
                     <td style='text-align:center'> Sex</td>
                    <td style='text-align:center'> Age</td>
                    <td style='text-align:center'> Blood Group</td>
                   <td style='text-align:center'> Email</td>
                    <td style='text-align:center'> Phone</td>
                    <td style='text-align:center'> Address</td>
                    <td style='text-align:center'> Update</td>
                    <td style='text-align:center'> Delete</td>
                </tr>";
            $count=0;
            $name_ch="name$count";
            $sex_ch="sex$count";
            $age_ch="age$count";
            $blood_ch="blood$count";
            $em_ch="em$count";
            $tel_ch="tel$count";
            $add_ch="add$count";
            $user_ch="user$count";
            $type_ch="type$count";
            $pass_ch="pass$count";
            $dep_ch="dep$count";
            $up_ch="up$count";
            $del_ch="del$count";
            
         while($record=mysqli_fetch_array($mydata))
         {
             //echo $record['Product']."<br/>";
             $name=$record['Name'];
             $sex=$record['Sex'];
             $age=$record['Age'];
             $blood=$record['Blood_Group'];
             $em=$record['Email_Id'];
             $tel=$record['Telephone_No'];
             $add=$record['Address'];
             $user=$record['User_Id'];
             $type=$record['User_Type'];
             $pass=$record['Password'];
             $dep=$record['Department'];
             if($type=='Accountant')
             echo "<tr><td  style='text-align:center' name=$user_ch value=$user size='10'>$user</td><td><input type=text style='text-align:center'  name=$name_ch value='$name' size='15'></td><td><input type=text style='text-align:center'  name=$sex_ch value=$sex size='6'></td><td><input type=text style='text-align:center'  name=$age_ch value=$age size='3'></td><td><input type=text style='text-align:center'  name=$blood_ch value=$blood size='5'></td><td><input type=text style='text-align:center'  name=$em_ch value=$em size='15'></td><td><input type=text style='text-align:center'  name=$tel_ch value=$tel size='12'></td><td><input type=text style='text-align:center'  name=$add_ch value='$add' size='20'></td><td><input type=submit name=$up_ch value=Update style='background-color:green;font-size:18px;color:white'></td><td><input type=submit name=$del_ch value=Remove style='background-color:red;font-size:18px;color:white'></td></tr>";
             $count=$count+1;
             $name_ch="name$count";
            $sex_ch="sex$count";
            $age_ch="age$count";
            $blood_ch="blood$count";
            $em_ch="em$count";
            $tel_ch="tel$count";
            $add_ch="add$count";
            $user_ch="user$count";
            $type_ch="type$count";
            $pass_ch="pass$count";
            $dep_ch="dep$count";
            $up_ch="up$count";
            $del_ch="del$count";
         }
             echo "</table>";
             echo "<input type=submit value='Add Accountant' name='add_ac' style='background-color:blue;font-size:18px;color:white'/>";
                     echo "</div></body></form>"; 
         
        }
        elseif(isset($_POST['log_out']))
        {
            echo "<script type='text/Javascript'>
            alert('Successfully Logged Out')</script>";
            $_SESSION['selected']=0;
            header("refresh:1 url=login_new.html");
        }
        elseif(isset($_POST['info']))
        {
            //echo "Personal information Selected";
         
            $sql="SELECT * FROM profile";
         $mydata=mysqli_query($link,$sql);
                $pass="";
                $sex="";
                $age="";
                $blood="";
                 $em="";
                 $tel="";
                 $address="";
                
         while($record=mysqli_fetch_array($mydata))
         {
             if($_SESSION['userid']==$record['User_Id'])
             {
                 $pass=$record['Password'];
                 $sex=$record['Sex'];
                $age=$record['Age'];
                $blood=$record['Blood_Group'];
                 $em=$record['Email_Id'];
                 $tel=$record['Telephone_No'];
                 $address=$record['Address'];
             }
             
         }
            
            echo "<form action=update_info.php method=post>";
            echo "<body style='margin: 0em auto;background-color:#E0FFFF'><div style='height:15px;width:1400px;background-color:teal;'></div><div style='height:100px;width:1400px;background-color:teal;text-align:center;float:left'><h1 style='color:white;font-size:35px'>PERSONAL INFORMATION</h1></div><div style='height:40px;width:1400px;float:left;background-color:#E0FFFF'></div><div style='height:700px;width:515px;float:left'></div><div style='float:center'>";
            echo "<table border=1 style='background-color:#F5FFFA;font-size:24px'>
                  <tr> 
                    <td style='color:red;font-weight:bold'> User Id</td><td>".$_SESSION['userid']."</td></tr><tr><td style='color:red;font-weight:bold'> Name</td><td>".$_SESSION['nameses']."</td></tr><tr><td style='color:red;font-weight:bold'> Password</td><td><input type=password name='passw' value=$pass size='20'></td></tr><tr><td style='color:red;font-weight:bold'> Sex </td><td><input type=text name='sex' value=$sex size='20'></td></tr><tr><td style='color:red;font-weight:bold'> Age </td><td><input type=text name='age' value=$age size='20'></td></tr><tr><td style='color:red;font-weight:bold'> Blood Group </td><td><input type=text name='bg' value=$blood size='20'></td></tr><tr><td style='color:red;font-weight:bold'> Email Id</td><td><input type=text name='eml' value=$em size='20'></td></tr><tr><td style='color:red;font-weight:bold'> Telephone No</td><td><input type=text name='tele' value=$tel size='20'></td></tr><tr><td style='color:red;font-weight:bold'> Address</td><td><input type=text name='addr' value='$address' size='20'></td></tr>
                    </table>";
             echo "<input type=submit value='Update' name='up_info' style='background-color:green;font-size:20px;color:white'/></div></body></form>";
        }
    }
?>