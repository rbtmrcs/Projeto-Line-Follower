#!/usr/bin/env python

import smach
import rospy
from std_msgs.msg import String
from serial_car import Car_control



rospy.init_node("maquina")

class Sinal(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['foi','repete'])
        self.sub = rospy.Subscriber('/sinalverde', String, self.callback)
        self.viu = False

    def callback(self, data):
        if data == String("vai"):
            self.viu = True

    def execute(self,userdata):
        rospy.sleep(2)
        if self.viu:
            return 'foi'
        else:
            return 'repete'


class Andarobj(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['foi','repete'])
        self.achou = False
        self.controle = Car_control()
        self.informacao = None
        self.jafoi = False

    def callback(self,data):
        if data == String('bate la'):
            self.achou = True

    def callback1(self,data):
        self.informacao = data

    def execute(self, ud):
        if not self.jafoi:
            self.sub = rospy.Subscriber('/bater', String, self.callback)
            self.sub1 = rospy.Subscriber('/andar1', String, self.callback1)
            self.jafoi = True
        rospy.sleep(2)
        if self.achou:
            return 'foi'

        if self.informacao is None:
            rospy.loginfo('??????')
            return 'repete'

        if self.informacao == String('frente'):
            rospy.loginfo('!!!!!')
            self.controle.pra_frente()

        elif self.informacao == String('direita'):
            rospy.loginfo('!!!!!')
            self.controle.direita_light()

        elif self.informacao == String('esquerda'):
            rospy.loginfo('!!!!!')
            self.controle.esquerda_light()

        elif self.informacao == String('muito direita'):
            rospy.loginfo('!!!!!')
            self.controle.direita_hard()

        elif self.informacao == String('muito esquerda'):
            rospy.loginfo('!!!!!')
            self.controle.esquerda_hard()
            
        return 'repete'

class Indoobj(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['foi','repete'])
        self.sub = rospy.Subscriber('/colidir', String, self.callback)
        self.sub = rospy.Subscriber('/andar3', String, self.callback1)
        self.chegou = False
        self.controle = Car_control()
        self.informacao = None

    def callback(self,data):
        if data == String('chegou'):
            self.chegou = True

    def callback1(self,data):
        self.informacao = data

    def execute(self, ud):
        rospy.sleep(2)
        if self.chegou:
            return 'foi'

        if self.informacao is None:
            rospy.loginfo('??????')
            return 'repete'

        if self.informacao == String('frente'):
            rospy.loginfo('!!!!!')
            self.controle.pra_frente()

        elif self.informacao == String('direita'):
            rospy.loginfo('!!!!!')
            self.controle.direita_light()

        elif self.informacao == String('esquerda'):
            rospy.loginfo('!!!!!')
            self.controle.esquerda_light()

        elif self.informacao == String('muito direita'):
            rospy.loginfo('!!!!!')
            self.controle.direita_hard()

        elif self.informacao == String('muito esquerda'):
            rospy.loginfo('!!!!!')
            self.controle.esquerda_hard()
            
        return 'repete'


class Reprocurar(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['foi','repete'])
        self.sub = rospy.Subscriber('/andar1', String, self.callback)
        self.back = False
        self.controle = Car_control()
    
    def callback(self,data):
        if data != String('nao achei'):
            self.back = True
    
    def execute(self, ud):
        rospy.sleep(2)
        self.controle.retroceder()
        if self.back:
            return 'foi'
        return 'repete'

class  Andarfinal(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['foi','repete'])
        
        self.parou = False
        self.controle = Car_control()
        self.informacao = None
        self.jafoi = False

    def callback(self,data):
        if data == String('para'):
            self.parou = True
    
    def callback1(self,data):
        self.informacao = data

    def execute(self, ud):
        if not self.jafoi:
            self.sub = rospy.Subscriber('/parar', String, self.callback)
            self.sub1 = rospy.Subscriber('/andar2', String, self.callback1)
            self.jafoi = True

        rospy.sleep(2)
        if self.parou:
            self.controle.pra_frente()
            rospy.sleep(4)
            self.controle.parar()
            return 'foi'

        if self.informacao is None:
            rospy.loginfo('??????')
            return 'repete'

        if self.informacao == String('frente'):
            rospy.loginfo('!!!!!')
            self.controle.pra_frente()

        elif self.informacao == String('direita'):
            rospy.loginfo('!!!!!')
            self.controle.direita_light()

        elif self.informacao == String('esquerda'):
            rospy.loginfo('!!!!!')
            self.controle.esquerda_light()

        elif self.informacao == String('muito direita'):
            rospy.loginfo('!!!!!')
            self.controle.direita_hard()

        elif self.informacao == String('muito esquerda'):
            rospy.loginfo('!!!!!')
            self.controle.esquerda_hard()
            
        return 'repete'

sm = smach.StateMachine(outcomes=['Acabou'])

with sm:
    smach.StateMachine.add('StandBy', Sinal(), transitions={'foi':'SeguindoLinhaObj','repete':'StandBy'})
    smach.StateMachine.add('SeguindoLinhaObj', Andarobj(), transitions={'foi':'IndoAteObj','repete':'SeguindoLinhaObj'})
    smach.StateMachine.add('IndoAteObj', Indoobj(), transitions={'foi':'ReProcurandoLinha','repete':'IndoAteObj'})
    smach.StateMachine.add('ReProcurandoLinha', Reprocurar(), transitions={'foi':'SeguindoLinhaFinal','repete':'ReProcurandoLinha'})
    smach.StateMachine.add('SeguindoLinhaFinal', Andarfinal(), transitions={'foi':'Acabou','repete':'SeguindoLinhaFinal'})

sm.execute()