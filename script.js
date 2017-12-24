(
function() {
    var getProjectSections = function() {
        return Array.from(document.querySelectorAll('.project'));
    };

    var getSectionLinks = function() {
        return Array.from(document.querySelectorAll('.project-link'));
    };

    var setFocusOnSectionLink = function(sectionId) {
        var links = getSectionLinks();

        links.forEach(function(l) { l.classList.remove('focus'); });

        var focusedEl = links.filter(function(x) { return x.id === sectionId + "Link"; })[0];

        focusedEl.classList.add('focus');
        
    };

    var focusedSection = '';

    var scrollEvent = function(e) {
        var sections = getProjectSections();
        var numSections = sections.length;

        
        var offsets = sections.map(function(s) { return s.getBoundingClientRect().top });

        //var bodyBottom = document.body.getBoundingClientRect().bottom;
        var height = window.innerHeight || document.body.clientHeight;

        var breakpoint = Math.max(height - 300, 0);
        var pastSections = offsets.map(function(o) { return o < breakpoint; })


        var overSection = numSections - 1 - pastSections
                            .reverse()
                            .findIndex(function(o) { return o; });

        console.log(overSection);
        
        var sectionId = sections[overSection].id;
        if(focusedSection !== sectionId) {
            focusedSection = sectionId;
            setFocusOnSectionLink(sectionId);
        }
    };

    window.addEventListener('scroll', scrollEvent);
    

}
)()


