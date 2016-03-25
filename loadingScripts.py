# encoding=utf8
from __future__ import unicode_literals
import MySQLdb
from django_expa import expaApi

def get_db():
    db = MySQLdb.connect(passwd="dashboardCOLOMBIA", user="dashboardadmin", host="aieseccolb.c76whjjr6x5k.us-west-2.rds.amazonaws.com", db="DASHBOARD", use_unicode=True)
    db.set_character_set('utf8')
    return db

def get_db_cursor(db):
    cursor = db.cursor()
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')
    return cursor


def load_world_performance():
    """
        Carga el desempeño de todas las oficinas del mundo que están cargadas en la base de datos, para los cuatro programas y el total
    """
    api = expaApi.ExpaApi()
    db = get_db()
    c = get_db_cursor(db)
    programs = ['IGCDP', 'OGCDP', 'IGIP', 'OGIP']
    metrics = ['applications', 'accepted', 'approved', 'realized', 'completed']
    c.execute("TRUNCATE TABLE STATS")
    c.execute("SELECT OFFICEExpaID, Nombre, Tipo FROM OFFICE WHERE Tipo='Region' OR Tipo='MC'") 
    #c.execute("SELECT OFFICEExpaID, Nombre, Tipo FROM OFFICE WHERE OFFICEexpaID = 1613") 
    db2 = get_db()
    c2 = get_db_cursor(db2)
    for office in c:
        if office[2] == 'Region':
	    print 'Cargando los datos de la región %s' % office[1]
	elif office[2] == 'MC':
	    print 'Cargando los datos del MC %s (id=%s)' % (office[1], office[0])
	    allProgramsPerformance = {}
	    for program in programs:
	        print "cargando %s" % program
		performance = api.getCountryCurrentMCYearStats(program, office[0])
                print performance
		for officeID, values in performance.iteritems():
                    try:
                        c2.execute("INSERT INTO STATS VALUES (%s, %s, %s, %s, %s, %s, %s)", (officeID, program, values['applications'], values['accepted'], values['approved'], values['realized'], values['completed']))
                    except MySQLdb.IntegrityError as e:
                        lcs = api.getSuboffices(office[0])
                        for lcTemp in lcs:
                            if lcTemp['id'] == officeID:
                                lc = lcTemp
                        c2.execute("INSERT INTO OFFICE VALUES (%s, %s, 'LC', %s)", (int(lc['id']), lc['name'], int(office[0])))
                        c2.execute("INSERT INTO STATS VALUES (%s, %s, %s, %s, %s, %s, %s)", (officeID, program, values['applications'], values['accepted'], values['approved'], values['realized'], values['completed']))
                        print "Nuevo LC agregado"
    db2.commit()
    c2.close()
    db2.close()
    db.commit()
    c.close()
    db.close()



def loadAllOffices():
    api = expaApi.ExpaApi()
    db = get_db()
    c = get_db_cursor(db)
    regions = api.getRegions()
    for region in regions:
    	print "Agregando la región %s" % region['name']
        c.execute("INSERT INTO OFFICE VALUES (%s, %s, 'Region', Null)", (int(region['id']), region['name']))
        mcs = api.getSuboffices(region['id'])
        for mc in mcs:
	    print "Agregando el MC %s" % mc['name']
            c.execute("INSERT INTO OFFICE VALUES (%s, %s, 'MC', %s)", (int(mc['id']), mc['name'], int(region['id'])))
	    lcs = api.getSuboffices(mc['id'])
	    for lc in lcs:
	        print "Agregando el LC %s" % lc['name']
	        c.execute("INSERT INTO OFFICE VALUES (%s, %s, 'LC', %s)", (int(lc['id']), lc['name'], int(mc['id'])))
    db.commit()
    c.close()
    db.close()
    print "Committed changes to DB, all connections closed"
        
if __name__ == "__main__":
    load_world_performance()
