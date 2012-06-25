# -*- coding:  utf-8 -*-

import logging

from plone.i18n.normalizer import idnormalizer #sirve para normalizar el lenguaje
from Products.ATContentTypes.lib import constraintypes #retrige el tipo de contenido a una carpeta
from Products.CMFPlacefulWorkflow.PlacefulWorkflowTool import WorkflowPolicyConfig_id

logger = logging.getLogger('misitio.utility')

def set_workflow_policy(obj):
    """Cambiar el workflow del objeto utilizando CMFPlacefulWorkflow.
    """
    product = 'CMFPlacefulWorkflow'
    obj.manage_addProduct[product].manage_addWorkflowPolicyConfig()
    pc = getattr(obj, WorkflowPolicyConfig_id)
    pc.setPolicyIn(policy='one-state')
    logger.info('Workflow changed for element %s' % obj.getId())

def createLink(context,title,link,
               exclude_from_nav=False):
    """Crea y publica un vinculo en el contexto dado"""
    oid = idnormalizer.normalize(title, 'es')
    if not hasattr(context, oid):
        context.invokeFactory('Link', id=oid, title=title, remoteUrl=link)
        link = context[oid]
        if exclude_from_nav:
            link.setExcludeFromNav(True)
        link.reindexObject()

def createDocument(context, title):
    """Crea y publica un documento (página) en el contexto dado.
    """
    oid = idnormalizer.normalize(title, 'es')
    if not hasattr(context, oid):
        context.invokeFactory('Document', id=oid, title=title)
        document = context[oid]
        document.reindexObject()

def createFolder(context, title, allowed_types=['Topic', 'Folder', 'Document'],
                 exclude_from_nav=False):
    """Crea una carpeta en el contexto especificado y modifica su política de
    workflows; por omisión, la carpeta contiene colecciones (Topic) y no
    modifica la política de workflow del contenido creado dentro de ella.
    """
    oid = idnormalizer.normalize(title, 'es')
    if not hasattr(context, oid):
        context.invokeFactory('Folder', id=oid, title=title)
        folder = context[oid]
        folder.setConstrainTypesMode(constraintypes.ENABLED)
        folder.setLocallyAllowedTypes(allowed_types)
        folder.setImmediatelyAddableTypes(allowed_types)
        set_workflow_policy(folder)
        if exclude_from_nav:
            folder.setExcludeFromNav(True)
        folder.reindexObject()
    else:
        folder = context[oid]
        folder.setLocallyAllowedTypes(allowed_types)
        folder.setImmediatelyAddableTypes(allowed_types)
        # reindexamos para que el catálogo se entere de los cambios
        folder.reindexObject()
