$(function(){
    $('#btn_next').click(function(){
        var seaion_id, name, phone;
        
        $("#alert1").hide();
        $("#alert2").hide();

        session_id=$("#session_id").val();
        name=$("#name").val().trim();
        phone=$("#phone").val().trim();


        if (name.length==0){
            $("#alert2_text").text('请输入姓名');
            $("#alert1").show();
            return;
        }

        if (phone.length==0){
            $("#alert2_text").text('请输入手机号');
            $("#alert1").show();
            return;
        }

        $("#btn1").hide();
        $("#wait_gif").show();

        $.ajax({
            type: "POST",
            url: "/wx/signup/next",
            async: true,
            timeout: 15000,
            data: {session_id:session_id,name:name,phone:phone},
            dataType: "json",
            complete: function(xhr, textStatus)
            {
                if(xhr.status==200){
                    var retJson = JSON.parse(xhr.responseText);
                    if (retJson["ret"]==0){
                        $("#text_name").text(retJson["data"]["name"]);
                        $("#text_phone").text(retJson["data"]["phone"]);
                        $("#block1").hide();
                        $("#block2").show();
                        $("#wait_gif").hide();
                    }
                    else{
                        $("#alert2_text").text(retJson["msg"]);
                        $("#alert1").show();
                        $("#btn1").show();
                        $("#wait_gif").hide();
                    }
                }
                else{
                    $("#alert2_text").text("网络异常！请稍后再试");
                    $("#alert1").show();
                    $("#btn1").show();
                    $("#wait_gif").hide();
                }
            }
        });

    });
});


$(function(){
    $('#btn_signup').click(function(){
        var session_id, name, phone, company, 
            title, position, dinner, lunch, checkin;
        
        $("#alert1").hide();
        $("#alert2").hide();

        session_id=$("#session_id").val();
        name=$("#name").val().trim();
        phone=$("#phone").val().trim();
        company=$("#company").val().trim();
        title=$("#title").val().trim();
        position=$("#position").val().trim();
        dinner = $('input[name=dinner]:checked').val();
        lunch = $('input[name=lunch]:checked').val();
        checkin = $('input[name=checkin]:checked').val();


        if (company.length==0){
            $("#alert2_text").text('请输入工作单位');
            $("#alert1").show();
            return;
        }

        if (title.length==0){
            $("#alert2_text").text('请输入职称');
            $("#alert1").show();
            return;
        }

        if (dinner==undefined){
            $("#alert2_text").text('请选择是否参加晚宴');
            $("#alert1").show();
            return;
        }

        if (lunch==undefined){
            $("#alert2_text").text('请选择是否需要午餐');
            $("#alert1").show();
            return;
        }

        if (checkin==undefined){
            $("#alert2_text").text('请选择是否需要安排入住');
            $("#alert1").show();
            return;
        }

        $("#btn2").hide();
        $("#wait_gif").show();

        $.ajax({
            type: "POST",
            url: "/wx/signup/done",
            async: true,
            timeout: 15000,
            data: {session_id:session_id,name:name,phone:phone,company:company,
                title:title,position:position,dinner:dinner,lunch:lunch,checkin:checkin},
            dataType: "json",
            complete: function(xhr, textStatus)
            {
                if(xhr.status==200){
                    var retJson = JSON.parse(xhr.responseText);
                    if (retJson["ret"]==0){
                        $("#block2").hide();
                        $("#alert2").show();
                        $("#wait_gif").hide();
                    }
                    else{
                        $("#alert2_text").text(retJson["msg"]);
                        $("#alert1").show();
                        $("#btn2").show();
                        $("#wait_gif").hide();
                    }
                }
                else{
                    $("#alert2_text").text("网络异常！请稍后再试");
                    $("#alert1").show();
                    $("#btn2").show();
                    $("#wait_gif").hide();
                }
            }
        });

    });
});

