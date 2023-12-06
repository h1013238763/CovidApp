index = 1;
const panel_list = ["sign_in_panel", "register_panel", "forget_panel", "reset_panel"];
user = "";
quest1 = "";
quest2 = "";

let userObject ={} // user object to store user information after sign in => {username, email} 


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
            window.location.href = '/survey';
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
    var is_empty = false;
    
    const data = {
        username: document.getElementById("register_username_input").value,
        password: document.getElementById("register_password_input").value,
        email: document.getElementById("register_email_input").value,
        question1: document.getElementById("register_question_1_input").value,
        answer1: document.getElementById("register_answer_1_input").value,
        question2: document.getElementById("register_question_2_input").value,
        answer2: document.getElementById("register_answer_2_input").value,
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

    if(data.username == "")
    {
        is_empty = true;
        document.getElementById("register_username_info").textContent = "Please enter content";
    }
    else
    {
        document.getElementById("register_username_info").textContent = "";
    }
    if(data.password == "")
    {
        is_empty = true;
        document.getElementById("register_password_info").textContent = "Please enter content";
    }
    else
    {
        document.getElementById("register_password_info").textContent = "";
    }
    if(data.email == "")
    {
        is_empty = true;
        document.getElementById("register_email_info").textContent = "Please enter content";
    }
    else
    {
        document.getElementById("register_email_info").textContent = "";
    }
    if(document.getElementById("register_confirm_input").value == "")
    {
        is_empty = true;
        document.getElementById("register_confirm_info").textContent = "Please enter content";
    }
    else
    {
        document.getElementById("register_confirm_info").textContent = "";
    }
    if(data.question1 == "")
    {
        is_empty = true;
        document.getElementById("register_question_1_info").textContent = "Please enter content";
    }
    else
    {
        document.getElementById("register_question_1_info").textContent = "";
    }
    if(data.answer1 == "")
    {
        is_empty = true;
        document.getElementById("register_answer_1_info").textContent = "Please enter content";
    }
    else
    {
        document.getElementById("register_answer_1_info").textContent = "";
    }
    if(data.question2 == "")
    {
        is_empty = true;
        document.getElementById("register_question_2_info").textContent = "Please enter content";
    }
    else
    {
        document.getElementById("register_question_2_info").textContent = "";
    }
    if(data.answer2 == "")
    {
        is_empty = true;
        document.getElementById("register_answer_2_info").textContent = "Please enter content";
    }
    else
    {
        document.getElementById("register_answer_2_info").textContent = "";
    }

    if(is_illegal || is_empty)
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
            console.log(data);
            console.log(result);
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
        username: document.getElementById("forget_username_input").value
    };

    if(data.username == "")
    {
        document.getElementById("forget_username_info").textContent = "Please enter your username";
        return;
    }

    fetch("http://127.0.0.1:5000/api/forgot_password", {
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
            console.log(result);
            // transfer to user page
            SwitchPanel(3);
        } 
        else
        {
            console.log("false");
            document.getElementById("forget_username_info").textContent = "username not exist";
        }  
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function ResetEvent()
{
    const data = {
        answer:document.getElementById("reset_code_input").value,
        username:document.getElementById("forget_email_input").value,
        password: document.getElementById("reset_password_input").value
    };

    var is_empty = false;
    var is_illegal = false;

    // username check
    if(data.username.length < 6 || data.username.length > 12)
    {
        document.getElementById("reset_username_info").style.color = "#ff6565";
        is_illegal = true;
    }
    else
    {
        document.getElementById("reset_username_info").style.color = "gray";
    }
    // password check
    if(data.password.length < 6 || data.password.length > 12)
    {
        document.getElementById("reset_password_info").style.color = "#ff6565";
        is_illegal = true;
    }
    else
    {
        document.getElementById("reset_password_info").style.color = "gray";
    }
    // password confirm check
    if(document.getElementById("reset_confirm_input").value !== data.password)
    {
        document.getElementById("reset_confirm_info").textContent = "password confirmation is incorrect";
        is_illegal = true;
    }
    else
    {
        document.getElementById("reset_confirm_info").textContent = "";
    }

    if(username == "")
    {
        is_empty = true;
        document.getElementById("reset_username_info").textContent = "Please enter content";
    }
    else
    {
        document.getElementById("reset_username_info").textContent = "";
    }
    if(password == "")
    {
        is_empty = true;
        document.getElementById("reset_password_info").textContent = "Please enter content";
    }
    else
    {
        document.getElementById("reset_password_info").textContent = "";
    }
    if(securityAnswer == "")
    {
        is_empty = true;
        document.getElementById("reset_answer_info").textContent = "Please enter content";
    }
    else
    {
        document.getElementById("reset_answer_info").textContent = "";
    }

    if(is_illegal || is_empty)
    {
        return;
    }

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
            console.log(result);
            SwitchPanel(0);
        } 
        else
        {
            console.log("true");
            document.getElementById("reset_answer_info").textContent = "security answer wrong";
        }  
    })
    .catch(error => {
        console.error('Error:', error);
    });
}