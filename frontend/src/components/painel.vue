<template>
    <div>
         <div class="col-auto">
            <div class="bg-light border rounded mb-5 p-2 painel">
                <h3 class="text-center">{{data.name}}</h3>
                <div class="m-auto text-center" v-if="data.online=='True'"><img :src="motorImg" height="160px"></div>
                <div class="m-auto text-center" v-else><img :src="getImgUrl('motorOffLine')" height="160px"></div>
                <b-form-group class="m-2" label="Eixo X(mm/s):" label-for="x">
                    <b-form-input v-model="data.vibraX" class="text-center text-primary" name="x" disabled size="lg" type="text"></b-form-input>
                </b-form-group>
                <b-form-group class="m-2" label="Eixo Z(mm/s):" label-for="z">
                    <b-form-input v-model="data.vibraZ" class="text-center text-primary" name="z" disabled size="lg" type="text"></b-form-input>
                </b-form-group>
                <b-form-group class="m-2" label="Temperatura(Cº):" label-for="temp">
                    <b-form-input v-model="data.temp" class="text-center text-primary" name="temp" disabled size="lg" type="text"></b-form-input>
                </b-form-group>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "painel",
    created(){
      this.load()
      setInterval(()=>{this.load()},2000)
    },
    data(){
      return{
          data:{}
      }
    },
    methods:{
        load(){
            this.readData()
        },
        getImgUrl(pet) {
            var images = require.context('../assets/', false, /\.png$/)
            return images('./' + pet + ".png")
        },
        async readData() {
        fetch('/nodes/',{
                method: 'get',
                headers: {
                    'Content-Type': 'application/json',
                }
        }).then(res=>{
            if(res.status === 200){
                return res.text()
            }
        }).then(result=>{
             this.data = JSON.parse(result)
             this.erro= false
        }).catch(erro=>{
            console.log(erro)
            this.erro= true
        })
      },
    },
    computed:{
      motorImg(){
          switch (this.data.estado) {
              case "OK":
                  return this.getImgUrl("motorOk")
                case "falha":
                  return this.getImgUrl("motorFalha")
                 case "alerta":
                  return this.getImgUrl("motorAlerta")
              default:
                  return this.getImgUrl("motorPreto")
          }
        }
    },
    props:{
    },
}
</script>

