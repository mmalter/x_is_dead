def default_checker(framework):
    def fun(d):
        script = """
        if(!!window.%s)
        {
            return true;
        } else {
            return false;
        }
        """ % framework
        o = d.execute_script(script)
        d.implicitly_wait(1)
        return o
    return fun

def angular_checker(d):
    script = """
    if(
    !!window.angular ||
    !!document.querySelector('script[src*="angular.js"], script[src*="angular.min.js"]') ||
    document.querySelector('.ng-binding, [ng-app], [data-ng-app], [ng-controller], [data-ng-controller], [ng-repeat], [data-ng-repeat]')
    )

    {
        return true;
    } else {
        return false;
    }
    """
    o = d.execute_script(script)
    d.implicitly_wait(1)
    return o

def react_checker(d):
    script = """
    if(
    !!window.React ||
    !!document.querySelector('[data-reactroot], [data-reactid]')
    )

    {
        return true;
    } else {
        return false;
    }
    """
    o = d.execute_script(script)
    d.implicitly_wait(1)
    return o

frameworks = {
        "JQuery" : default_checker("jQuery"),
        "React" : react_checker,
        "Angular" : angular_checker,
        "Ember" : default_checker("Ember"),
        "Vue" : default_checker("Vue"),
        "Meteor" : default_checker("Meteor"),
        "Zepto" : default_checker("Zepto")
        }
