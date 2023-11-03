index = 1;
const panel_list = ["sign_in_panel", "register_panel", "forget_panel", "reset_panel"];

// Sign Page Image Change Functions
function ChangeImage()
{
  var div = document.getElementById("image_button_panel");
  var baseUrl = div.getAttribute("data-url");
  var image = document.getElementById("show_image");

  image.style.opacity = 0;
  setTimeout(function () {
    image.src = baseUrl + index + ".jpg";
    image.style.opacity = 1;
  }, 800);

    var button = document.getElementById("image_button_"+index);
    button.style.width = 45;

    other_index = index
    for(i = 0; i < 2; i ++)
    {
        other_index ++;
        if(other_index > 3)
        {
            other_index =1
        }
        document.getElementById("image_button_"+other_index).style.width = 20;
    }
}
function ChangeImageIndex(image_index)
{
    index = image_index;
    ChangeImage();
}
function ChangeIndex()
{
    index++;
    if(index > 3)
    {
        index = 1;
    }
    ChangeImage();
}
var image_change_interval = setInterval(ChangeIndex, 10000);

// Panel Switch Functions
function SwitchPanel(panel_index)
{  
    for(i = 0; i < panel_list.length; i ++)
    {
        if(i == panel_index)
        {
            document.getElementById(panel_list[i]).style.display='grid';
        }
        else
        {
            document.getElementById(panel_list[i]).style.display='none';
        }
    }
}


// Sign in Button event
function SigninEvent()
{
    console.log("sign in 1");

    const data = {
        username: document.getElementById("sign_username_input").value,
        password: document.getElementById("sign_password_input").value
    };

    // input content handler
    var is_empty = false;
    // console.log("username["+document.getElementById("sign_username_input").value+"]");
    if(data.username == "")
    {
        document.getElementById("sign_username_info").textContent = "please enter username";
        is_empty = true;
    }
    else
    {
        document.getElementById("sign_username_info").textContent = "";
    }
    // console.log("password["+document.getElementById("sign_password_input").value+"]");
    if(data.password == "")
    {
        document.getElementById("sign_password_info").textContent = "please enter password";
        is_empty = true;
    }
    else
    {
        document.getElementById("sign_password_info").textContent = "";
    }
    if(is_empty)
    {
        return;
    }

    fetch("http://127.0.0.1:5000/api/login", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data),
        redirect : "follow"
    })
    .then(response => response.json())
    .then(result => {
        if(result.userAuthenticated)
        {
            console.log("true");
            // transfer to user page
            window.location.href = 'SurveyPage.html';
        } 
        else
        {
            console.log("true");
            document.getElementById("sign_password_info").textContent = "wrong password";
        }  
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Create Account Button event
function CreateAccountEvent()
{
    console.log("create 1");
    // input content handler
    var is_illegal = false;
    
    const data = {
        username: document.getElementById("register_username_input").value,
        password: document.getElementById("register_password_input").value,
        email: document.getElementById("register_email_input").value
    };
    // username check
    if(data.username.length < 6 || data.username.length > 12)
    {
        document.getElementById("register_username_info").style.color = "#ff6565";
        is_illegal = true;
    }
    else
    {
        document.getElementById("register_username_info").style.color = "gray";
    }
    // email check
    if(data.email.indexOf('@') !== -1 && data.email.indexOf('.') !== -1)
    {
        if( data.email.indexOf('@') >= data.email.indexOf('.'))
        {
            document.getElementById("register_email_info").textContent = "please enter vaild email";
            is_illegal = true;
        }
        else
        {
            document.getElementById("register_email_info").textContent = "";
        }
    }
    else
    {
        document.getElementById("register_email_info").textContent = "please enter vaild email";
        is_illegal = true;
    }
    // password check
    if(data.password.length < 6 || data.password.length > 12)
    {
        document.getElementById("register_password_info").style.color = "#ff6565";
        is_illegal = true;
    }
    else
    {
        document.getElementById("register_password_info").style.color = "gray";
    }
    // password confirm check
    if(document.getElementById("register_confirm_input").value !== data.password)
    {
        document.getElementById("register_confirm_info").textContent = "password confirmation is incorrect";
        is_illegal = true;
    }
    else
    {
        document.getElementById("register_confirm_info").textContent = "";
    }

    if(is_illegal)
    {
        return;
    }

    console.log("create 2");
    // transfer data

    fetch("http://127.0.0.1:5000/api/create_account", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data),
        redirect : "follow"
    })
    .then(response => response.json())
    .then(result => {
        if(result.userAuthenticated)
        {
            console.log("true");
            SwitchPanel(0);
        } 
        else
        {
            console.log("true");
            document.getElementById("register_email_info").textContent = "email or username is already in use";
        }  
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function ForgetEvent()
{
    const data = {
        email: document.getElementById("forget_email_input").value
    };

    var is_illegal = false;

    if(data.email.indexOf('@') !== -1 && data.email.indexOf('.') !== -1)
    {
        if( data.email.indexOf('@') >= data.email.indexOf('.'))
        {
            document.getElementById("forget_email_info").textContent = "please enter vaild email";
            is_illegal = true;
        }
        else
        {
            document.getElementById("forget_email_info").textContent = "";
        }
    }
    else
    {
        document.getElementById("forget_email_info").textContent = "please enter vaild email";
        is_illegal = true;
    }

    if(is_illegal)
    {
        return;
    }

    if(ServerResponseTrue(data))
    {
        SwitchPanel(3);
    }
    else
    {
        console.log('Authentication fail');
    }
}

function ResetEvent()
{
    const data = {
        email:document.getElementById("forget_email_input").value,
        code:document.getElementById("reset_code_input").value,
        password: document.getElementById("reset_password_input").value
    };
}

function ServerResponseTrue(data, url)
{
    fetch(url, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data),
        redirect : "follow"
    })
    .then(response => response.json())
    .then(result => {
        if(result.userAuthenticated)
        {
            console.log("true");
            return true;
        } 
        else
        {
            console.log("true");
            return false;
        }  
    })
    .catch(error => {
        console.error('Error:', error);
    });
}