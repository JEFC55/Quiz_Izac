# Aplicativo Quiz Linguagem Python
# Necessário Instalar Bibliotecas Kivy KivyMD através do comando:
# pip install kivy kivymd
# www.bgmax.com.br
# Desenvolvido por Wilson Borges de Oliveira

import platform
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.core.audio import SoundLoader

# Dicionário com perguntas e alternativas
perguntas = {
    "1. Qual é o objetivo principal em *The Binding of Isaac*?": {
        "A. Coletar moedas e comprar itens": False,
        "B. Derrotar inimigos e chefes enquanto avança por andares": True,
        "C. Completar puzzles para progredir na história": False,
        "D. Construir uma base e defender-se de invasores": False,
        "E. Explorar o mundo e conversar com NPCs": False
    },
    "2. O que são *Tears* no jogo?": {
        "A. Poções de cura": False,
        "B. Ataques que Isaac dispara contra os inimigos": True,
        "C. Itens colecionáveis": False,
        "D. Moedas usadas para comprar itens": False,
        "E. Inimigos especiais": False
    },
    "3. O que acontece quando Isaac perde todos os corações?": {
        "A. Ele ganha uma vida extra automaticamente": False,
        "B. O jogo termina e você precisa recomeçar": True,
        "C. Ele recupera parte da vida após alguns segundos": False,
        "D. Ele perde apenas metade de seus itens": False,
        "E. O jogo pausa até que ele recupere vida": False
    },
    "4. Qual é a função da sala dourada em *The Binding of Isaac*?": {
        "A. Conter inimigos poderosos para derrotar": False,
        "B. Oferecer um item gratuito por andar": True,
        "C. Fornecer uma loja cheia de itens": False,
        "D. Conceder um coração extra": False,
        "E. Conter moedas e chaves": False
    },
    "5. O que são *Soul Hearts* em *The Binding of Isaac*?": {
        "A. Corpos de inimigos que Isaac pode absorver": False,
        "B. Corações temporários que não podem ser regenerados": True,
        "C. Corações que aumentam permanentemente a vida de Isaac": False,
        "D. Itens consumíveis que restauram toda a vida": False,
        "E. Corações usados para realizar *Devil Deals*": False
    }
}

class TelaQuiz(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sound = SoundLoader.load('sound.mp3')
        if self.sound:
            self.sound.play()

        self.indice_pergunta = 0
        self.pontuacao = 0
        self.label_pontuacao = MDLabel(
            text=f"Pontuação: {self.pontuacao}", 
            halign="center", 
            theme_text_color="Custom", 
            text_color=(1, 1, 1, 1), 
            pos_hint={'center_x': 0.5, 'center_y': 0.05}
        )
        self.exibir_pergunta()

    def exibir_pergunta(self):
        self.clear_widgets()

        # Layout principal
        layout = FloatLayout()

        sistema = platform.system()
        if sistema == 'Windows':
            # Configura a tela para um tamanho específico em sistemas Windows
            Window.size = (720/2, 1280/2)

        # Adiciona a imagem de fundo
        img_fundo = Image(source="./fundo.png", allow_stretch=True, keep_ratio=False, size_hint=(1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        layout.add_widget(img_fundo)

        if self.indice_pergunta < len(perguntas):
            # Exibe a pergunta no topo com cor branca
            pergunta_texto = list(perguntas.keys())[self.indice_pergunta]
            pergunta_label = MDLabel(
                text=pergunta_texto, 
                halign="center", 
                theme_text_color="Custom", 
                text_color=(1, 1, 1, 1),  # Cor branca (R, G, B, A)
                font_style="H5", 
                size_hint=(1, None), 
                height=100, 
                pos_hint={'center_x': .5, 'center_y': .8}
            )
            layout.add_widget(pergunta_label)

            # Adiciona as opções de resposta na parte inferior
            for idx, (resposta, correta) in enumerate(perguntas[pergunta_texto].items()):
                btn = MDRaisedButton(text=resposta, size_hint=(.8, None), height=50, pos_hint={'center_x': .5, 'y': 0.65 - idx * 0.1})
                btn.bind(on_release=lambda instance, correta=correta: self.verificar_resposta(correta))
                layout.add_widget(btn)

            # Remove o label de pontuação do layout anterior, se necessário, antes de adicionar novamente
            if self.label_pontuacao.parent:
                self.label_pontuacao.parent.remove_widget(self.label_pontuacao)

            # Adiciona o label de pontuação ao rodapé
            layout.add_widget(self.label_pontuacao)

        else:
            # Exibe a pontuação final em branco
            layout.add_widget(MDLabel(
                text=f"Sua pontuação final: {self.pontuacao}", 
                halign="center", 
                theme_text_color="Custom", 
                text_color=(1, 1, 1, 1),  # Cor branca
                font_style="H5", 
                pos_hint={'center_x': 0.5, 'center_y': 0.6}
            ))

            # Adiciona o botão para sair do aplicativo
            btn_sair = MDRaisedButton(
                text="Sair", 
                size_hint=(.5, None), 
                height=50, 
                pos_hint={'center_x': 0.5, 'center_y': 0.4}
            )
            btn_sair.bind(on_release=self.sair_app)
            layout.add_widget(btn_sair)

        self.add_widget(layout)

    def verificar_resposta(self, correta):
        resultado = "Você Acertou!" if correta else "Você Errou!"
        if correta:
            self.pontuacao += 20
        self.label_pontuacao.text = f"Pontuação: {self.pontuacao}"
        self.exibir_popup(resultado)

    def exibir_popup(self, resultado):
        layout_popup = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Definindo a cor branca para o texto do popup
        label_resultado = MDLabel(
            text=resultado, 
            halign="center", 
            theme_text_color="Custom", 
            text_color=(1, 1, 1, 1)  # Cor branca (R, G, B, A)
        )

        btn_fechar = MDRaisedButton(text="Fechar", size_hint=(1, None), height=50)
        layout_popup.add_widget(label_resultado)
        layout_popup.add_widget(btn_fechar)

        popup = Popup(title="Resultado", content=layout_popup, size_hint=(0.75, 0.5))
        btn_fechar.bind(on_release=popup.dismiss)
        popup.bind(on_dismiss=lambda _: self.proxima_pergunta())
        popup.open()

    def proxima_pergunta(self):
        self.indice_pergunta += 1
        self.exibir_pergunta()

    def sair_app(self, instance):
        MDApp.get_running_app().stop()

class AppQuiz(MDApp):
    def build(self):      
        sm = ScreenManager()
        sm.add_widget(TelaQuiz(name="quiz"))
        return sm

if __name__ == '__main__':
    AppQuiz().run()
