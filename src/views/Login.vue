<template>
  <div class="login-container">
    <div class="login-background">
      <el-form :model="ruleForm2" :rules="rules2" ref="ruleForm2" label-position="left" label-width="0px" class="demo-ruleForm login-holder">
        <!-- <el-form ref="loginForm" :model="loginForm" :rules="loginRules" class="login-form" auto-complete="on" label-position="left"> -->
        <h3 class="title">系统登录</h3>
        <el-form-item prop="account">
          <el-input type="text" v-model="ruleForm2.account" auto-complete="off" placeholder="账号"></el-input>
        </el-form-item>
        <el-form-item prop="checkPass">
          <el-input type="password" v-model="ruleForm2.checkPass" auto-complete="off" placeholder="密码"></el-input>
        </el-form-item>
        <el-checkbox v-model="checked" checked class="remember">记住密码</el-checkbox>
        <el-form-item style="width:100%;">
          <el-button type="primary" style="width:100%;" @click.native.prevent="handleSubmit2" :loading="logining">登录</el-button>
        </el-form-item>
      </el-form>
      <div class="tips">
        <span style="margin-right:20px;">Copyright @ 润电能源科学技术有限公司 </span>
        <span> http://www.crepri.com</span>
      </div>
    </div>
  </div>
</template>

<script>
  import { requestLogin } from '../api/api';
  export default {
   data() {
      return {
        logining: false,
        ruleForm2: {
          account: 'admin',
          checkPass: '123456789'
        },
        rules2: {
          account: [
            { required: true, message: '请输入账号', trigger: 'blur' },
          ],
          checkPass: [
            { required: true, message: '请输入密码', trigger: 'blur' },
          ]
        },
        checked: true
      };
    },
    mounted() {
			var token = sessionStorage.getItem('token');
			if (token) {
        sessionStorage.setItem('token', token);
        this.$router.push({ path: '/table' });
      }
    },
    methods: {
      handleSubmit2(ev) {
        var _this = this;
        this.$refs.ruleForm2.validate((valid) => {
          if (valid) {
            this.logining = true;
            //NProgress.start();
            var loginParams = { username: this.ruleForm2.account, password: this.ruleForm2.checkPass };
            requestLogin(loginParams).then(data => {
              this.logining = false;
              //NProgress.done();
              let { msg, code, token, name } = data;
              if (code !== 200) {
                this.$message({
                  message: msg,
                  type: 'error'
                });
              } else {
                this.$message({
                  message: msg,
                  type: 'success'
                });
                sessionStorage.setItem('token', JSON.stringify(token));
                sessionStorage.setItem('name', JSON.stringify(name));
                this.$router.push({ path: '/table' });
              }
            });
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      }
    }
  }

</script>

// <style lang="scss" scoped>
//   .login-holder {
//     /*box-shadow: 0 0px 8px 0 rgba(0, 0, 0, 0.06), 0 1px 0px 0 rgba(0, 0, 0, 0.02);*/
//     -webkit-border-radius: 5px;
//     border-radius: 5px;
//     // -moz-border-radius: 5px;
//     // background-clip: padding-box;
//     margin: 180px auto;
//     width: 350px;
//     top :500px;
//     padding: 35px 35px 15px 35px;
//     background: rgba(255,255,255,0.5); // 最后一个参数设置透明度
//     border: 1px solid #eaeaea;
//     box-shadow: 0 0 25px #cac6c6;
//     .title {
//       margin: 0px auto 40px auto;
//       text-align: center;
//       color: #505458;
//     }
//     .remember {
//       margin: 0px 0px 35px 0px;
//     }
//   }
// </style>

<style lang="scss" scoped>
$bg:#2d3a4b;
$dark_gray:#889aa4;
$light_gray:#eee;

.login-background {
  width: 100%;
  height: 585px;
  // height: 100%;
  background: url('../assets/loginbg.jpg') no-repeat;
  background-size: cover;

}
.login-holder {
    // box-shadow: 0 0px 8px 0 rgba(0, 0, 0, 0.06), 0 1px 0px 0 rgba(0, 0, 0, 0.02);
    -webkit-border-radius: 5px;
    border-radius: 5px;
    -moz-border-radius: 5px;
    // background-clip: padding-box;
    margin: 180px auto;
    width: 350px;
    top :500px;
    padding: 35px 35px 15px 35px;
    background: rgba(255,255,255,0.5); // 最后一个参数设置透明度
    border: 1px solid #eaeaea;
    box-shadow: 0 0 25px #cac6c6;
    .title {
      margin: 0px auto 40px auto;
      text-align: center;
      color: #505458;
    }
    .remember {
      margin: 0px 0px 35px 0px;
    }
}

.tips {
    font-size: 14px;
    color: #fff;
    position: relative;
    left: 430px;
    // top: 80px;
    margin-bottom: 10px;
    span {
      &:first-of-type {
        margin-right: 16px;
      }
    }
}
.login-container {
  min-height: 80%;
  width: 100%;
  background-color: $bg;
  overflow: hidden;
  top: 0px;

  // .login-form {
  //   position: relative;
  //   width: 500px;
  //   max-width: 100%;
  //   padding: 160px 35px 0;
  //   margin: 0 auto;
  //   overflow: hidden;
  // }

  // .svg-container {
  //   padding: 6px 5px 6px 15px;
  //   color: $dark_gray;
  //   vertical-align: middle;
  //   width: 30px;
  //   display: inline-block;
  // }

  // .title-container {
  //   position: relative;
  //   top: 35px;
  //   right: 135px;
  //   .title {
  //     font-size: 26px;
  //     color: $light_gray;
  //     margin: 0px auto 40px auto;
  //     text-align: center;
  //     font-weight: bold;
  //   }
  // }

  // .show-pwd {
  //   position: absolute;
  //   right: 10px;
  //   top: 7px;
  //   font-size: 16px;
  //   color: $dark_gray;
  //   cursor: pointer;
  //   user-select: none;
  // }
}
</style>