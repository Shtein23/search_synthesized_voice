var socket = io();
socket.on('connect', function() {
    socket.emit('my event', {data: 'I\'m connected!'});
    socket.emit('join', {room: 'testing'});

    socket.on('joined', function (data){
        console.log(data)
    })
    $(document).ready(function () {
        let epoch = 0
        let max_batch = 0
        socket.on('file', function (data){
            $('#store2').css({"display": "none"})
            $('#store').css({"display": "none"}).html('').css({"display": "block"})
            for (var i = 0; i < data["files"].length; i++) {
                $('#store').append('<button data-target="'+data["target"]+'" style="margin: 0.3em">'+data["files"][i]+'</button><br>')
            }

            if (data["models"] != 0){
                $('#store2').html('').css({"display": "block"})
                for (var i = 0; i < data["models"].length; i++) {
                    $('#store2').append('<div class="form-check">\n' +
                        '<input class="form-check-input" type="radio" name="flexRadioDefault" id="flexRadioDefault1">\n' +
                        '<label class="form-check-label" for="flexRadioDefault1">'+data["models"][i]+
                        '</label>' +
                        '</div>')
                }
            }

        })

        socket.on('start_train', function (data){
            // console.log(data)
            $('#main').append('<div class="extract">' +
                '<p>Обработка данных</p><div class="progress">' +
                '<div class="prog progress-bar progress-bar-striped progress-bar-animated bg-success" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="'+data["max"]+'" style="width: 0%"></div>' +
                '<div class="err progress-bar progress-bar-striped progress-bar-animated bg-success" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="'+data["max"]+'" style="width: 0%"></div>' +
                '</div></div>')
            $('.test').css({"display": "none"})
            $('.loader').css({"display": "block"})
        })

        socket.on('inprogress', function (data){
            // console.log(data)
            $('.prog').attr('aria-valuenow', data["point"]).css({width: ((data["point"]/data["max"])*100).toFixed(3)+'%'}).text(((data["point"]/data["max"])*100).toFixed(3)+'%')
            $('.err').attr('aria-valuenow', data["err"]).css({width: ((data["err"]/data["max"])*100).toFixed(3)+'%'}).text(((data["err"]/data["max"])*100).toFixed(3)+'%')
            $('.test').css({"display": "none"})
            $('.loader').css({"display": "block"})
        })
        socket.on('end_extract', function (){
            $('.extract').remove()
        })
        socket.on('start_epoch', function (data){
            $('.test').css({"display": "none"})
            $('.loader').css({"display": "block"})
            epoch = data['epoch']+1
            max_batch = data['max_batch']
            $('.epoch'+epoch-1).removeClass('progress-bar-animated')
            $('#main').append('<br><div id="epoch'+epoch+'"><p>Эпоха обучения модели - '+ epoch +'/5</p>' +
                'batch: <span class="batch"></span>/'+max_batch +
                '<div class="progress">' +
                '<div class="epoch'+epoch+' progress-bar progress-bar-striped progress-bar-animated" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="'+max_batch+'" style="width: 0%"></div>' +
                '</div>' +
                'loss: <span class="loss"></span><br> ' +
                ' accuracy: <span class="accuracy"></span>' +
                '</div>')
        })

        socket.on('prog_train', function (data) {
            $('#epoch'+epoch+' .batch').text(data['batch'])
            $('#epoch'+epoch+' .loss').text(data['loss'].toFixed(3))
            $('#epoch'+epoch+' .accuracy').text(data['accuracy'].toFixed(3))
            $('.epoch'+epoch).attr('aria-valuenow', data["batch"]).css({width: ((data["batch"]/max_batch)*100).toFixed(3)+'%'}).text(((data["batch"]/max_batch)*100).toFixed(3)+'%')
        });

        socket.on('end_train', function (){
            $('div[id^="epoch"]').remove()
            $('.test').css({"display": "block"})
            $('.loader').css({"display": "none"})
        })


        socket.on('create_stat', function (data){
            $('#store2').html('<p>'+data["name"]+'</p>' +
                '<img style="width: 100%" src="' + data['img'] + '">' +
                '<p>Точность = '+ (100 - (data["eer"].toFixed(2)*1)) + '%' +
                '<br>EER = '+data["eer"].toFixed(2)+'%' +
                '<br>Threshold = '+data["tr"].toFixed(4)+'</p>').css({"display": "block"})

        })

        $('#train').on('click', function (){
            socket.emit('train')
        })
        $('#check').on('click', function (){
            socket.emit('check')
        })
        $('#stat').on('click', function (){
            socket.emit('stat')
        })

        $('#store').on('click', 'button', function (){
            socket.emit('do_this', {"name": $(this).text(), "target": $(this).attr('data-target')})
        })

    });
});

