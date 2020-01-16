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
        rospy.loginfo("Entrou no callback")
        rospy.loginfo("DADOS >{}<".format(data))
        rospy.loginfo(type(data))

        if data == String("vai"):
            rospy.loginfo("!!!!!!!!!!")
            self.viu = True

    def execute(self,userdata):
        rospy.sleep(2)
        rospy.loginfo(self.viu)
        if self.viu:
            return 'foi'
        else:
            return 'repete'


class Andarobj(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['foi','repete'])
        self.sub = rospy.Subscriber('/bater', String, self.callback)
        self.sub1 = rospy.Subscriber('/andar1', String, self.callback1)
        self.achou = False
        self.controle = Car_control()
        self.informacao = None

    def callback(self,data):
        print (data)
        if data == 'bate la':
            self.achou = True

    def callback1(self,data):
        self.informacao = data

    def execute(self, ud):
        if self.achou:
            return 'foi'

        if self.informacao is None:
            return 'repete'

        if self.informacao == 'frente':
            self.controle.pra_frente()

        elif self.informacao == 'direita':
            self.controle.direita_light()

        elif self.informacao == 'esquerda':
            self.controle.esquerda_light()

        elif self.informacao == 'muito direita':
            self.controle.direita_hard()

        elif self.informacao == 'muito esquerda':
            self.controle.esquerda_hard()
            
        return 'repete'

class  Andarfinal(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['foi','repete'])
        self.sub = rospy.Subscriber('/hrdeparar', String, self.callback)
        self.sub1 = rospy.Subscriber('/andar2', String, self.callback1)
        self.parou = False
        self.informacao1 = None

    def callback(self,data):
        print (data)
        if data == 'anda um pouco e para':
            self.parou = True
    
    def callback1(self,data):
        self.informacao1 = data

    def execute(self, ud):
        if self.parou:
            return 'foi'

        if self.informacao is None:
            return 'repete'

        if self.informacao == 'frente':
            self.controle.pra_frente()

        elif self.informacao == 'direita':
            self.controle.direita_light()

        elif self.informacao == 'esquerda':
            self.controle.esquerda_light()

        elif self.informacao == 'muito direita':
            self.controle.direita_hard()

        elif self.informacao == 'muito esquerda':
            self.controle.esquerda_hard()
            
        return 'repete'

sm = smach.StateMachine(outcomes=['Deu'])

with sm:
    smach.StateMachine.add('StandBy', Sinal(), transitions={'foi':'SeguindoLinhaObj','repete':'StandBy'})
    smach.StateMachine.add('SeguindoLinhaObj', Andarobj(), transitions={'foi':'SeguindoLinhaFinal','repete':'SeguindoLinhaObj'})
    #smach.StateMachine.add('IndoAteObj', Andar2(), transitions={'foi':'ReProcurandoLinha','repete':'IndoAteObj'})
    #smach.StateMachine.add('ReProcurandoLinha', Virar(), transitions={'foi':'SeguindoLinhaFinal','repete':'ReProcurandoLinha'})
    smach.StateMachine.add('SeguindoLinhaFinal', Andarfinal(), transitions={'foi':'StandBy','repete':'SeguindoLinhaFinal'})

sm.execute()