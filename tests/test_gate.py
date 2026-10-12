from scripts.collect import credible, event_key, canonical

def valid():
 return dict(eligible=True,allegation_qualified=True,victim_is_minor=False,victim_identifying_details=False,suspect_identifying_details=False,neighborhood='Merkez',district='Şişli',province='İstanbul',incident_date='2026-10-10',locality_evidence='Merkez Mahallesi',official_confirmation=True,confidence=.97,category='domestic_violence')
def test_high_confidence(): assert credible(valid())
def test_child_blocked():
 d=valid();d['victim_is_minor']=True;assert not credible(d)
def test_no_neighborhood_blocked():
 d=valid();d['neighborhood']='';assert not credible(d)
def test_no_official_blocked():
 d=valid();d['official_confirmation']=False;assert not credible(d)
def test_date_group_key(): assert '2026 10 10' in event_key(valid())
def test_canonical(): assert canonical('https://example.com/a?utm_source=x')=='https://example.com/a'
