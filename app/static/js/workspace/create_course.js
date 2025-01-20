document.addEventListener('DOMContentLoaded', function() {
    // Initialize Summernote
    $('.summernote').summernote({
        height: 200,
        toolbar: [
            ['style', ['style']],
            ['font', ['bold', 'underline', 'clear']],
            ['color', ['color']],
            ['para', ['ul', 'ol', 'paragraph']],
            ['table', ['table']],
            ['insert', ['link']],
            ['view', ['fullscreen', 'codeview', 'help']]
        ]
    });
});

function addContentSection(type) {
    const template = document.getElementById('contentSectionTemplate');
    const clone = template.content.cloneNode(true);
    const section = clone.querySelector('.content-section');
    const contentFields = section.querySelector('.content-fields');
    const typeLabel = section.querySelector('.content-type-label');
    
    section.dataset.type = type;
    
    // Set the content type label
    const labels = {
        'video': 'Video Content',
        'document': 'Document',
        'link': 'External Link',
        'text': 'Text Tutorial'
    };
    typeLabel.textContent = labels[type];
    
    // Add fields based on content type
    switch(type) {
        case 'video':
            contentFields.innerHTML = `
                <div class="mb-3">
                    <label class="form-label">Video Title</label>
                    <input type="text" class="form-control" name="content[${getContentIndex()}][title]" required>
                </div>
                <div class="mb-3">
                    <label class="form-label">Video File</label>
                    <input type="file" class="form-control" name="content[${getContentIndex()}][file]" accept="video/*" required>
                </div>
                <div class="mb-3">
                    <label class="form-label">Description</label>
                    <textarea class="form-control" name="content[${getContentIndex()}][description]" rows="2"></textarea>
                </div>
                <input type="hidden" name="content[${getContentIndex()}][type]" value="video">
            `;
            break;
            
        case 'document':
            contentFields.innerHTML = `
                <div class="mb-3">
                    <label class="form-label">Document Title</label>
                    <input type="text" class="form-control" name="content[${getContentIndex()}][title]" required>
                </div>
                <div class="mb-3">
                    <label class="form-label">Document File</label>
                    <input type="file" class="form-control" name="content[${getContentIndex()}][file]" accept=".pdf,.doc,.docx,.ppt,.pptx" required>
                </div>
                <div class="mb-3">
                    <label class="form-label">Description</label>
                    <textarea class="form-control" name="content[${getContentIndex()}][description]" rows="2"></textarea>
                </div>
                <input type="hidden" name="content[${getContentIndex()}][type]" value="document">
            `;
            break;
            
        case 'link':
            contentFields.innerHTML = `
                <div class="mb-3">
                    <label class="form-label">Link Title</label>
                    <input type="text" class="form-control" name="content[${getContentIndex()}][title]" required>
                </div>
                <div class="mb-3">
                    <label class="form-label">URL</label>
                    <input type="url" class="form-control" name="content[${getContentIndex()}][url]" required>
                </div>
                <div class="mb-3">
                    <label class="form-label">Description</label>
                    <textarea class="form-control" name="content[${getContentIndex()}][description]" rows="2"></textarea>
                </div>
                <input type="hidden" name="content[${getContentIndex()}][type]" value="link">
            `;
            break;
            
        case 'text':
            contentFields.innerHTML = `
                <div class="mb-3">
                    <label class="form-label">Tutorial Title</label>
                    <input type="text" class="form-control" name="content[${getContentIndex()}][title]" required>
                </div>
                <div class="mb-3">
                    <label class="form-label">Content</label>
                    <textarea class="form-control content-editor" name="content[${getContentIndex()}][content]" rows="5"></textarea>
                </div>
                <input type="hidden" name="content[${getContentIndex()}][type]" value="text">
            `;
            // Initialize Summernote for the new text content
            $(contentFields.querySelector('.content-editor')).summernote({
                height: 200,
                toolbar: [
                    ['style', ['style']],
                    ['font', ['bold', 'underline', 'clear']],
                    ['color', ['color']],
                    ['para', ['ul', 'ol', 'paragraph']],
                    ['table', ['table']],
                    ['insert', ['link', 'picture']],
                    ['view', ['fullscreen', 'codeview', 'help']]
                ]
            });
            break;
    }
    
    document.getElementById('contentSections').appendChild(section);
}

function removeContentSection(button) {
    const section = button.closest('.content-section');
    if (section) {
        // Destroy Summernote instance if it exists
        const editor = section.querySelector('.content-editor');
        if (editor) {
            $(editor).summernote('destroy');
        }
        section.remove();
    }
}

function getContentIndex() {
    return document.querySelectorAll('.content-section').length;
}
