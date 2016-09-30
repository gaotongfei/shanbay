/*
maybe re-implement function :hideUnrelated: to function :showRelated: and add class :hidden: for eacg
 */
$(document).ready(function(){
    hideUnrelated();
});

function hideUnrelated() {
    var word = $('.word');
    //var first_word = word[0];
    var rest_words = word.slice(1);

    for (var i=0; i<rest_words.length; i++) {
        rest_words.addClass('hidden');
    }
}

function getIdNum(clicked_id) {
    var currentIdNum = parseInt(clicked_id.split('-').pop());
    var nextIdNum = currentIdNum + 1;
    return [currentIdNum, nextIdNum];
}

function handle_result(result, clicked_id, data_id) {
    var idNum = getIdNum(clicked_id);
    var currentIdNum = idNum[0];
    var nextIdNum = idNum[1];
    console.log('current: ' + currentIdNum);
    console.log('next: ' + nextIdNum);

    // when currentIdNum is the max number it could get, do something


    // show translation
    var notHiddenEle = $('.word:not(".hidden") > div.detail');
    notHiddenEle.removeClass('hidden');

    // hide options
    var optionKnownEle = $('.options > #indexId-' + currentIdNum);
    var optionUnknownEle = $('.options > #unknown-' + currentIdNum);

    optionKnownEle.addClass('hidden');
    optionUnknownEle.addClass('hidden');

    // show next button
    var nextBtn = $('#indexId-' + currentIdNum).find('.next');
    nextBtn.removeClass('hidden');

    if (result == 'known') {
        // handle ajax request when 'known' this word
        handleKnownWords(data_id)
    } else {
        // handle ajax request when doesn't know
    }


}

function next(clicked_id, words_per_day) {
    var idNum = getIdNum(clicked_id);
    var currentIdNum = idNum[0];
    var nextIdNum = idNum[1];

    var currentEle = $('#indexId-'+currentIdNum);
    var nextEle = $('#indexId-'+nextIdNum);

    currentEle.addClass('hidden');
    nextEle.removeClass('hidden');

    if (currentIdNum === words_per_day) {
        // redirect to home page with post data if current word is the last
        $.redirect('/', {'words_per_day': words_per_day, 'message': 'finished'});
    }
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


