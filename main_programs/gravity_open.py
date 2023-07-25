import math
import pygame
pygame.init()

LARGURA, ALTURA =  1600, 1000
WIN = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('teste de troca de QDM')

#cores
branco = (255,255,255)
preto = (0,0,0)
azul_escuro = (10,10,46)
amarelo = (255,255,0)
verde_lima = (50,205,50)
ciano = (65,105,255)
bronze = (205,127,50)
vermelho_mercurio = (124,22,40)
azul_netuno = (10,53,121)
azul_urano = (10,227,224)
laranja = (212,73,0)

FONT = pygame.font.SysFont('comicsans', 16)

G = 6.67428e-11 #gravitational constant

e = 0.7 #coeficiente de restituição/ restitution coefficient

u = 0.8 #coeficiente de absorção/ absorption coefficient

novos_blocos0 = []

class Bloco:
    def __init__(self,x,y,cor,massa,raio,x_vel,y_vel):
        self.existe = True
        self.x = x
        self.y = y
        self.cor = cor
        self.massa = massa
        self.raio = raio

        self.orbit = []

        self.x_vel = x_vel
        self.y_vel = y_vel


    def draw(self, win):
        x = self.x + LARGURA/2
        y = self.y + ALTURA/2    

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:  #da lista orbit pegamos cada ponto
                x, y = point
                x = x + LARGURA/2
                y = y + ALTURA/2
                updated_points.append((x,y))
        
            pygame.draw.lines(win, self.cor, False, updated_points, 2)

        pygame.draw.circle(win, self.cor, (x,y), self.raio)

        velx_text = FONT.render(f"Vx={round(self.x_vel,2)}m/s", 1, branco)
        win.blit(velx_text, (x - velx_text.get_width()*1.5, y - velx_text.get_height()*1.5))
        vely_text = FONT.render(f"Vy={round(self.y_vel,2)}m/s", 1, branco)
        win.blit(vely_text, (x - vely_text.get_width()*1.5, y - vely_text.get_height()*3))
        x_text = FONT.render(f"X={round(self.x,2)}m", 1, branco)
        win.blit(x_text, (x - x_text.get_width()*-0.5, y - x_text.get_height()*-1.5))
        y_text = FONT.render(f"Y={round(self.y,2)}m", 1, branco)
        win.blit(y_text, (x - y_text.get_width()*-0.5, y - y_text.get_height()*-3))
        ax_text = FONT.render(f"Ax={round(self.ax,6)}m/s^2", 1, branco)
        win.blit(ax_text, (x - x_text.get_width()*-1, y - x_text.get_height()*-2))
        ay_text = FONT.render(f"Ay={round(self.ay,6)}m/s^2", 1, branco)
        win.blit(ay_text, (x - x_text.get_width()*-1, y - x_text.get_height()*-4))
    
    def update_position(self,blocos):
        total_fx = total_fy = 0
        for bloco in blocos:
                if bloco==self:
                     continue
            
                fx, fy = atracao(self,bloco)
                total_fx += fx
                total_fy += fy
        
        self.ax = total_fx/self.massa
        self.ay = total_fy/self.massa

        self.x_vel += self.ax
        self.y_vel += self.ay

        self.x += self.x_vel 
        self.y += self.y_vel 

        self.orbit.append((self.x, self.y))

def create_object(x,y,cor,massa,raio,x_vel,y_vel,lista):
    novo_bloco = Bloco(x,y,cor,massa,raio,x_vel,y_vel)
    lista.append(novo_bloco)


    
def delete(bloco,blocos):
    blocos.remove(bloco)

def consumir(bloco,other):
    if other.massa<1000:
        bloco.massa+=other.massa
    else:    
        bloco.massa+=u*other.massa
    other.existe = False

        

def colisao(bloco,other):
        distancia_critica = math.fabs(bloco.raio + other.raio)
        distance_x = math.fabs(bloco.x - other.x)
        distance_y = math.fabs(bloco.y - other.y)
        distance = math.sqrt(distance_x**2 + distance_y**2)
        if (bloco.x_vel<0 and other.x_vel<0) or (bloco.x_vel>0 and other.x_vel>0):
            vrelx = bloco.x_vel + other.x_vel
        else:
            vrelx = bloco.x_vel - other.x_vel

        if (bloco.y_vel<0 and other.y_vel<0) or (bloco.y_vel>0 and other.y_vel>0):
            vrely = bloco.y_vel + other.y_vel
        else:
            vrely = bloco.y_vel - other.y_vel
        
        xvel1 = bloco.x_vel
        xvel2 = other.x_vel

        yvel1 = bloco.y_vel
        yvel2 = other.y_vel
        

        if distance<=distancia_critica:
            if bloco.massa>=10**5*other.massa or other.massa>=bloco.massa*10**5:
                e=0
            else:
                e=1
            bloco.x_vel = (bloco.massa*xvel1 + other.massa*xvel2 - other.massa*vrelx*e)/(bloco.massa+other.massa) #para x
            other.x_vel = vrelx*e-math.fabs(bloco.x_vel) #para x

            bloco.y_vel = (bloco.massa*yvel1 + other.massa*yvel2 - other.massa*vrely*e)/(bloco.massa+other.massa) #para y
            other.y_vel = vrely*e-math.fabs(bloco.y_vel) #para y
            

            return True
        
def atracao(bloco,other):
        distancia_critica = math.fabs(bloco.raio + other.raio)
        distance_x = math.fabs(bloco.x - other.x)
        distance_y = math.fabs(bloco.y - other.y)
        distance = math.sqrt(distance_x**2 + distance_y**2)
        if distance <= distancia_critica:
            F = 0
            if other.massa>=10**10 and bloco.massa>=10**10:
                other.existe = False
                bloco.existe = False
                create_object((bloco.x+other.x)/2,(bloco.y+other.y)/2,preto,bloco.massa+other.massa,(bloco.raio+other.raio)/2,0,0,novos_blocos0)

            elif bloco.massa>10**3*other.massa:
                if other.massa>=1000:
                    consumir(bloco,other)
                    create_object(other.x,other.y,other.cor,other.massa*(1-u),other.raio/(1+u),1.2*math.sqrt(G*bloco.massa/(bloco.raio+other.raio)),1.2*math.sqrt(G*bloco.massa/(bloco.raio+other.raio)),novos_blocos0)
                else: 
                    consumir(bloco,other)
                
            elif other.massa>bloco.massa*10**3:
                if bloco.massa>=1000:
                    consumir(other,bloco)
                    create_object(bloco.x,bloco.y,bloco.cor,bloco.massa*(1-u),bloco.raio/(1+u),1.2*math.sqrt(G*other.massa/(bloco.raio+other.raio)),1.2*math.sqrt(G*other.massa/(bloco.raio+other.raio)),novos_blocos0)
                else: 
                    consumir(bloco,other)
            

        else:
            F = G*bloco.massa*other.massa/distance**2 # força gravitacional newtoniana
            
        teta = math.atan2(distance_y, distance_x) # ângulo teta definido pela função inversa da tangente da distância entre os blocos em y e em x

        #lidar com os sinais das componentes da força gravitacional devido ausencia de vetores
        if bloco.x<other.x:
            F_x =  math.cos(teta) * F #componente x da força gravitacional
        else:
            F_x =  math.cos(teta) * -F 
        if bloco.y<other.y:
            F_y = math.sin(teta) * F #componente y da força gravitacional
        else:
            F_y = math.sin(teta) * -F 
        return F_x, F_y


def main():
    run = True
    clock = pygame.time.Clock()

    bloco1 = Bloco(0,0,amarelo,10**14,30,0,0)
    bloco2 = Bloco(-600,-200,verde_lima,10**13,20,-2,1)
    bloco3 = Bloco(-500,200,laranja,10**9,10,-2,1)
    bloco4 = Bloco(650,-300,ciano,10**9,10,-2,3)
    bloco5 = Bloco(-400,-30,vermelho_mercurio,10**9,10,0.3,0.5)

    blocos = [bloco1,bloco2,bloco3,bloco4,bloco5]
    massa_total = 0
    for bloco in blocos:
        massa_total+=bloco.massa
    print(f'o sistema tem massa total de {massa_total}')
    novos_blocos = novos_blocos0
    qblocos = len(blocos)
    

    maior_raio = 0
    for bloco in blocos:
        if bloco.raio>maior_raio:
            maior_raio=bloco.raio
    
    n=0    

    while run:
        clock.tick(60)
        WIN.fill(azul_escuro)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if len(novos_blocos)>=1:
            blocos.append(novos_blocos[0])
            novos_blocos.clear()

        for bloco in blocos:
            if not bloco.existe:
                delete(bloco,blocos)
            else:
                bloco.update_position(blocos)
                bloco.draw(WIN)
                for other_bloco in blocos:
                    if other_bloco == bloco:
                        continue
                    else:
                        if colisao(bloco,other_bloco)==True:
                            n+=1

        n_text = FONT.render(f"{n}", 1, branco)                
        WIN.blit(n_text, (10,10))



        pygame.display.update()

    pygame.quit()
    i=1
    for bloco in blocos:
        print(f'o bloco {i} tem massa de {bloco.massa}')
        i+=1

main()