if (jQuery != undefined) {
    var django = {
        'jQuery':jQuery
    }
}

(function() {
    var global = this;
    var $ = django.jQuery;
    var console = global.console || {log: function() {}};
    
    var AjaxUploadWidget = global.AjaxUploadWidget = function(element, options) {
        
        /*if( $.browser.msie ){
            alert( $.browser.version );
        }*/
        
        this.options = {
            previewAreaClass: 'preview-area',
            previewFilenameLength: 20,
            showProgress: false,
            onUpload: null, // right before uploading to the server
            onComplete: null,
            onError: null,
            onRemove: null
        };
        $.extend(this.options, options);
        this.$element = $(element);
        this.initialize();
    };

    AjaxUploadWidget.prototype.DjangoAjaxUploadError = function(message) {
        this.name = 'DjangoAjaxUploadError';
        this.message = message;
    };
    AjaxUploadWidget.prototype.DjangoAjaxUploadError.prototype = new Error();
    AjaxUploadWidget.prototype.DjangoAjaxUploadError.prototype.constructor = AjaxUploadWidget.prototype.DjangoAjaxUploadError;

    AjaxUploadWidget.prototype.initialize = function() {
        var self = this;
        this.name = this.$element.attr('name');


        this.$element.wrap('<div class="ajax-uploader"></div>');

        // Create a hidden field to contain our uploaded file name
        this.$hiddenElement = $('<input type="hidden"/>')
            .attr('name', this.name)
            .val(this.$element.data('filename'));
        this.$element.attr('name', 'file'); // because we don't want to conflict with our hidden field
        this.$element.after(this.$hiddenElement);

        this.$loadingIndicator = $('<div class="loading"></div>');
        this.$loadingIndicator.hide();
        this.$element.before(this.$loadingIndicator);
        
        // Initialize preview area and action buttons
        this.$previewArea = $('<div class="'+this.options.previewAreaClass+'"></div>');
        this.$element.before(this.$previewArea);

        jQuery.data( document.body, "pararellUploadsCount", 0 );
        
        // Listen for when a file is selected, and perform upload
        this.inputId = this.$element.attr('id');
        this.$element.one('change', function(evt) {self.upload();});
                	
        //this.$changeButton = $('<label class="btn-change" for="' + this.$element.attr('id') + '" title="Upload New Image"></label>');
        //this.$element.after(this.$changeButton);

        this.$removeButton = $('<button type="button" class="btn-remove" title="Remove Image"></button>')
            .on('click', function(evt) {
                if(self.options.onRemove) {
                    var result = self.options.onRemove.call(self);
                    if(result === false) return;
                }
                self.$hiddenElement.val('');
                //from reasons unknown, file input was unaccessible whatever method used after using jquery iframe transport once
                // ... so here we are creating a brand new element and ignoring the old one.
                //newElement.click();
        
                self.displaySelection();
            });
        this.$element.after(this.$removeButton);
        this.$element.wrap('<div class="hiddenCheat"></div>');
        this.$elementParent = this.$element.parent();
        this.displaySelection();
    };
    
    AjaxUploadWidget.prototype.getElement = function() {
    	return this.$element;
    };
    
    AjaxUploadWidget.prototype.newRandomId = function() {
        this.inputId = "";
        for (i = 0; i < 32; i++) {
                this.inputId += Math.floor(Math.random() * 16).toString(16);
        }
    }
    
    AjaxUploadWidget.prototype.upload = function() {
    	//console.log('upload1');
    	//console.log(this.$element.val());
        var self = this;
        if(!this.$element.val()) return;
        if(this.options.onUpload) {
            var result = this.options.onUpload.call(this);
            if(result === false) return;
        }
        this.$element.attr('name', 'file');
        this.$element.parents('form').find('input[type=submit]').attr('disabled', 'disabled');
        this.$element.parents('form').find('button[type=submit]').attr('disabled', 'disabled');
        
        var pararellUploadsCount = jQuery.data( document.body, "pararellUploadsCount");
        pararellUploadsCount = pararellUploadsCount + 1;
        jQuery.data( document.body, "pararellUploadsCount", pararellUploadsCount);
                
        //console.log('upload2');
        this.$loadingIndicator.show();
        
        var url = this.$element.data('upload-url'); 
        if(this.options.showProgress){
        	this.uuid = "";
        	for (i = 0; i < 32; i++) {
        		this.uuid += Math.floor(Math.random() * 16).toString(16);
        	}
        	url = url + '?X-Progress-ID=' + this.uuid;
        	this.uploadMonitor = window.setInterval(function () {self.updateProgress();}, 1800);	
        }
        $.ajax(url, {
            iframe: true,
            files: this.$element,
            processData: false,
            type: 'POST',
            dataType: 'json',
            success: function(data) { self.postUpload(); self.uploadDone(data); },
            error: function(xhr, ajaxOptions, thrownError) { self.postUpload(); self.uploadFail(xhr, ajaxOptions, thrownError); }
        });
        
    };
    
    AjaxUploadWidget.prototype.updateProgress = function() {
         var self = this;
         req = new XMLHttpRequest();
         req.open("GET", "/uploadprogress", 1);
         req.setRequestHeader("X-Progress-ID", this.uuid);
         req.onreadystatechange = function () {
          if (req.readyState == 4) {
           if (req.status == 200) {
            /* poor-man JSON parser */
            var upload = eval(req.responseText);

            var txt = upload.state;

            /* change the width if the inner progress-bar */
            if (upload.state == 'done' || upload.state == 'uploading') {
              var p = Math.round(10000 * upload.received / upload.size) / 100;
              txt = txt + ' (' + p + '%)';
            }
            self.$loadingIndicator.text(txt);
            
            /* we are done, stop the interval */
            if (upload.state == 'done') {
             window.clearTimeout(self.uploadMonitor);
            }
           }
          }
         }
         req.send(null);
    }
    
    AjaxUploadWidget.prototype.postUpload = function() {
        if(this.options.showProgress){
           window.clearTimeout(this.uploadMonitor);
        }
    	//console.log('postUpload');
        this.$loadingIndicator.fadeOut();
    	//console.log(this.$hiddenElement.parents('form').find('input[type=submit]').length);
    	
    	var pararellUploadsCount = jQuery.data( document.body, "pararellUploadsCount");
        pararellUploadsCount = pararellUploadsCount - 1;
        jQuery.data( document.body, "pararellUploadsCount", pararellUploadsCount);
        if (pararellUploadsCount == 0) {
                this.$hiddenElement.parents('form').find('input[type=submit]').removeAttr('disabled');
                this.$hiddenElement.parents('form').find('button[type=submit]').removeAttr('disabled');
        }
        
        var self = this;
        self.newRandomId();
        self.$element = $('<input data-upload-url="/ajax-upload/" id="' + self.inputId + '" name="file" type="file"/>');
        self.$elementParent.html(self.$element);
        self.$element.one('change', function(evt) {self.upload();});
    
    }

    AjaxUploadWidget.prototype.uploadDone = function(data) {
    	//console.log('DONE');
        // This handles errors as well because iframe transport does not
        // distinguish between 200 response and other errors
        
        if(data.errors) {
            this.uploadFail({}, {}, data.errors);
        } else {
            this.$hiddenElement.val(data.path);
            //this.$element.val('');
            //var tmp = this.$element;
            //this.$element = this.$element.clone(true).val('');
            //tmp.replaceWith(this.$element);
            this.displaySelection();
            if(this.options.onComplete) this.options.onComplete.call(this, data.path);
        }
    };

    AjaxUploadWidget.prototype.uploadFail = function(xhr, status, error) {
    	alert('File uploading failed. Please make sure this is a valid file.');
        this.displaySelection();
        //console.log(xhr);
        //console.log(xhr.responseText);
        //console.log(status);
        //console.log(error);
    	/*
        if(this.options.onError) {
            this.options.onError.call(this);
        } else {
            //console.log('Upload failed:');
        }*/
    };

    AjaxUploadWidget.prototype.displaySelection = function() {
        var filename = this.$hiddenElement.val();
        var self = this;
        this.$previewArea.empty();
        this.$previewArea.append(this.generateFilePreview(filename));
        //this.$previewArea.find('.add-image-label').click(function(){
        //	return false;
        //});
        //this.$previewArea.show();
        if(filename !== '') {
        	this.$removeButton.show();
        } else {
            this.$removeButton.hide();
        }
    };

    AjaxUploadWidget.prototype.generateFilePreview = function(filename) {
        // Returns the html output for displaying the given uploaded filename to the user.
    	var output = '';
    	if (filename == '') {
    		output = '<label for="' + this.inputId + '" class="add-image-label">add image</label>';
    	} else {
	        var prettyFilename = this.prettifyFilename(filename);
	        output = $('<a href="'+filename+'" target="_blank"></a>');
	        var image = false;
	        $.each(['jpg', 'jpeg', 'png', 'gif'], function(i, ext) {
	            if(filename.toLowerCase().slice(-ext.length) == ext) {
	            	var $img = $('<img src="'+filename+'"/>');
	            	$img.load(function(){
	            		var mrg = (130 - $(this).height()) / 2;
	            		$(this).css('margin-top', (mrg + 5) + 'px');
	            		$(this).css('margin-bottom', mrg + 'px');
	            	});
	                output.append($img);
	    	        image = true;
	                return false;
	            }
	        });
	        if(!image){
                output.append('<img src="/static/ajax_upload/icons/other.png"/>');
	        }
	        output.append(prettyFilename);
	        if (typeof output.fancybox !== 'undefined')
	        {
	        	output.fancybox();
	        }
    	}
        return output;
    };

    AjaxUploadWidget.prototype.prettifyFilename = function(filename) {
        // Get rid of the folder names
        var cleaned = filename.slice(filename.lastIndexOf('/')+1);

        // Strip the random hex in the filename inserted by the backend (if present)
        var re = /^[a-f0-9]{32}\-/i;
        cleaned = cleaned.replace(re, '');

        // Truncate the filename
        var maxChars = this.options.previewFilenameLength;
        var elipsis = '...';
        if(cleaned.length > maxChars) {
            cleaned = cleaned.slice(0, 10) + elipsis + cleaned.slice((-1 * maxChars) + elipsis.length + 10);
        }
        return cleaned;
    };

    AjaxUploadWidget.autoDiscover = function(options) {
        $('input[type="file"].ajax-upload').each(function(index, element) {
            new AjaxUploadWidget(element, options);
        });
    };
}).call(this);
