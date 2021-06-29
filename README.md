# passenger-segmentation-using-smart-card-data
<!DOCTYPE html>
{% load static %}
<style>
    ul#menu {
        padding: 0
    }
    ul#menu li {
        display: inline;
    }
    ul#menu li a {
        background-color: #dd3535;
        color: #c9bdbd;
        padding: 5px 10px;
        text-decoration: none;
        font: 700 15px cursive;
        border-radius: 4px 4px 0 0;
    }
    ul#menu li a:hover {
        background-color: #c9bdbd;
        color: #dd3535;
        font: 700 18px fantasy;
        border-radius: 4px 4px 0 0;
    }
</style>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Route Stations</title>
</head>
<body>

<center>
    <h1 ><font color="#366092">Metro Ticket</font></h1>
    <ul id="menu">
        <li><a href="{% url 'admin_settings' %}">Home</a></li>
        <li><a href="{% url 'admin_station_master_view' %}">Station</a></li>
        <li><a href="{% url 'admin_route_master_view' %}">Route</a></li>
        <li><a href="{% url 'admin_changepassword' %}">Change Password</a></li>
        <li><a href="{% url 'admin_home' %}">Back</a></li>
    </ul>

    <h2><font color="#366092">Route Stations</font></h2>

    <form name="frm" action="{% url 'admin_route_details_add' %}" method="post">
            {% csrf_token %}
        <table>
            <tr>
	        <td>Station</td>
	        <td>
             	<select class="form-control" id="station_master_id"  name="station_master_id">
		            {% for  c in station_list%}
		        	<option value="{{c.id}}">{{c.station_name}}</option>
		            {% endfor %}
		        </select>
			</td>
	    </tr>
	        <tr>
	            <td>Stop No</td>
	            <td><input type="text"  name="stop_no" placeholder="Enter stop no" required="required"></td>
	        </tr>
            <tr>
	            <td></td>
	            <td><button type="submit" >SUBMIT</button></td>
	        </tr>
	    </table>
        {{msg}}
        <input type="hidden"  name="route_master_id" value="{{route_master_id}}" required="required">
    </form>

</center>
</body>
</html>
