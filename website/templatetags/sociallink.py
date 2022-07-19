from django import template
from website.models import SocialLinks, Team

register = template.Library()


@register.filter(name='get_link')
def get_link(team_id, lk):
    print(team_id)
    print(lk)
    team = Team.objects.get(id=team_id)

    l = SocialLinks.objects.filter(team=team)
    if lk == 't' and l.exists():
        l = l.first()
        if l.twitter:
            link = l.twitter
        else:
            link = ''
        return link
    elif lk == 'f' and l.exists():
        l = l.first()
        if l.facebook:
            link = l.facebook
        else:
            link = ''
        return link
    elif lk == 'lin' and l.exists():
        l = l.first()
        if l.linkedin:
            link = l.linkedin
        else:
            link = ''
        return link
    elif lk == 'ins' and l.exists():
        l = l.first()
        if l.instagram:
            link = l.linkedin
        else:
            link = ''
        return link
    else:
        return ''
