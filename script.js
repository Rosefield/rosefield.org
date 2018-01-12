(
function() {
    var getProjectSections = function() {
        return Array.from(document.querySelectorAll('.project'));
    };

    var getSectionLinks = function() {
        return Array.from(document.querySelectorAll('.project-link'));
    };
    var links = getSectionLinks();
    links.forEach(function(l) {
        
        l.onclick = function(e) { 
            setFocusOnSectionLink(l.id) 

        };
        });

    var setFocusOnSectionLink = function(id) {

        links.forEach(function(l) { l.classList.remove('focus'); });

        var focusedEl = links.filter(function(x) { return x.id === id + "Link" || x.id === id; })[0];

        focusedEl.classList.add('focus');
        
    };

    var sections = getProjectSections();

    var focusedSection = sections[0].id;
    setFocusOnSectionLink(focusedSection);

    var scrollEvent = function(e) {
        var numSections = sections.length;

        var offsets = sections.map(function(s) { return s.getBoundingClientRect().top });

        //var bodyBottom = document.body.getBoundingClientRect().bottom;
        var height = window.innerHeight || document.body.clientHeight;

        var breakpoint = Math.max(height - 300, 0);
        var pastSections = offsets.map(function(o) { return o < breakpoint; })


        var overSection = numSections - 1 - pastSections
                            .reverse()
                            .findIndex(function(o) { return o; });

        if(overSection >= numSections) {
            return;
        }
        
        var sectionId = sections[overSection].id;
        if(focusedSection !== sectionId) {
            focusedSection = sectionId;
            setFocusOnSectionLink(sectionId);
        }
    };


    window.addEventListener('scroll', scrollEvent);
    

}
)()


