function showFirstWord() {
    var first_word = $('.word').first();
    first_word.removeClass('hidden');
}

function getIdNum(clicked_id) {
    var currentIdNum = parseInt(clicked_id.split('-').pop());
    var nextIdNum = currentIdNum + 1;
    return [currentIdNum, nextIdNum];
}


// execute when use click "认识" or "不认识"
function handle_result(result, clicked_id, data_id) {
    var idNum = getIdNum(clicked_id);
    var currentIdNum = idNum[0];
    var nextIdNum = idNum[1];
    console.log('current: ' + currentIdNum);
    console.log('next: ' + nextIdNum);

    // show translation
    var notHiddenEle = $('.word:not(".hidden") > div.detail');
    notHiddenEle.removeClass('hidden');

    // show next button
    var buttonEle = $('#buttonId-'+currentIdNum);
    buttonEle.removeClass('hidden');

    // hide options
    var optionKnownEle = $('.options > #indexId-' + currentIdNum);
    var optionUnknownEle = $('.options > #unknown-' + currentIdNum);

    optionKnownEle.addClass('hidden');
    optionUnknownEle.addClass('hidden');

    if (result == 'known') {
        // handle ajax request when 'known' this word
        handleKnownWords(data_id);
    } else {
        // handle ajax request when doesn't know
    }

    // load notes here
    loadNotes(data_id, clicked_id);
}

function handleKnownWords(data_id) {
    var data = {};
    data['token'] = $('#token').val();
    data['word_id'] = data_id;

    if (data['token'] && data['word_id']) {
        data['message'] = 'success';
    } else {
        data['message'] = 'failed'
    }

    $.ajax({
        url: '/api/known',
        type: 'POST',
        data: data
    })
}

function next(clicked_id, words_per_day) {
    // do things when clicked next button
    var idNum = getIdNum(clicked_id);
    var currentIdNum = idNum[0];
    var nextIdNum = idNum[1];

    // hide current element and show next element
    var currentEle = $('#'+currentIdNum);
    var nextEle = $('#'+nextIdNum);

    console.log(currentEle);
    console.log(nextEle);

    currentEle.addClass('hidden');
    nextEle.removeClass('hidden');

    if (currentIdNum === words_per_day) {
        // redirect to home page with post data if current word is the last
        $.redirect('/', {'words_per_day': words_per_day, 'message': 'finished'});
    }
}

function loadNotes(data_id, clicked_id){
    var idNum = getIdNum(clicked_id);
    var currentIdNum = idNum[0];
    var data = {};
    data['word_id'] = data_id;
    data['token'] = $('#token').val();
    $.ajax({
        url: '/api/load_notes',
        type: 'POST',
        data: data,
        success: function(data) {
            var note = data['notes_info'];
            var noteEle = $('#note-'+currentIdNum);
            if (note.length == 0) {
                noteEle.html('<div class="alert alert-info" role="alert">暂无笔记, 来添加一条吧</div>');
            } else {
                console.log(data);
                var _html = "";
                for (var i=0; i<note.length; i++) {
                    _html +=
                        '<div class="panel panel-default"><div class="panel-body">' +
                        '<div class="note-username"><label>by: </label> ' + note[i]['username'] + '</div>' +
                        '<div class="note-content"><h4>' + note[i]['content'] + '</h4></div>' +
                        '<div class="note-created-time">' + note[i]['created_time'] + '</div>' +
                        '</div></div>'
                }
                noteEle.append(_html);
            }
        }
    });
}

function validateNoteTextarea() {
    $('#note-form').submit(function() {
        var noteText = $.trim($('#note-textarea').val());
        if (noteText === '') {
            alert('can not be null');
            return false;
        }
    })
}

$(document).ready(function(){
    // init: show first word
    showFirstWord();
    validateNoteTextarea();
});

