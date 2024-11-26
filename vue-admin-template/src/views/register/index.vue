<template>
    <div class="login-container">
        <el-form ref="registerForm" :model="registerForm" :rules="loginRules" class="login-form" auto-complete="on"
            label-position="left">

            <div class="title-container">
                <h3 class="title">注册</h3>
            </div>

            <el-form-item prop="username">
                <span class="svg-container">
                    <svg-icon icon-class="user" />
                </span>
                <el-input ref="username" v-model="registerForm.username" placeholder="用户名" name="username" type="text"
                    tabindex="1" auto-complete="on" />
            </el-form-item>
            <el-form-item prop="email">
                <span class="svg-container">
                    <svg-icon icon-class="email" />
                </span>
                <el-input ref="email" v-model="registerForm.email" placeholder="邮箱" name="email" type="text"
                    tabindex="1" auto-complete="on" />
            </el-form-item>
            <el-form-item prop="verifycode" style="width:70%;display: inline-block;">
                <span class="svg-container">
                    <svg-icon icon-class="verifycode" />
                </span>
                <el-input ref="verifycode" v-model="registerForm.verifycode" placeholder="验证码" name="verifycode"
                    type="text" tabindex="1" auto-complete="on" />
            </el-form-item>
            <el-button :loading="loading2" type="primary" style="width:30%;height: 52px;"
                @click.native.prevent="handleVerifyCode">发送验证码</el-button>
            <el-form-item prop="password">
                <span class="svg-container">
                    <svg-icon icon-class="password" />
                </span>
                <el-input :key="passwordType" ref="email" v-model="registerForm.password" :type="passwordType"
                    placeholder="密码" name="password" tabindex="2" auto-complete="on"
                    @keyup.enter.native="handleRegister" />
                <span class="show-pwd" @click="showPwd">
                    <svg-icon :icon-class="passwordType === 'password' ? 'eye' : 'eye-open'" />
                </span>

            </el-form-item>
            <el-form-item prop="checkpassword">
                <span class="svg-container">
                    <svg-icon icon-class="password" />
                </span>
                <el-input :key="passwordType2" ref="checkpassword" v-model="registerForm.checkpassword"
                    :type="passwordType2" placeholder="再次输入密码" name="checkpassword" tabindex="2" auto-complete="on"
                    @keyup.enter.native="handleRegister" />
                <span class="show-pwd" @click="showPwd2">
                    <svg-icon :icon-class="passwordType2 === 'password' ? 'eye' : 'eye-open'" />
                </span>

            </el-form-item>

            <el-button :loading="loading" type="primary" style="width:100%;margin-bottom:30px;"
                @click.native.prevent="handleRegister">注册</el-button>

            <div class="tips">
                <span> 已有账号?</span>
                <el-link type="primary" @click="gotoLogin">立即登录</el-link>
            </div>

        </el-form>
    </div>
</template>

<script>
// import { validUsername } from '@/utils/validate'
import { register, sendVerifyCode } from '@/api/user';
export default {
    name: 'Login',
    data() {

        var validatePass2 = (rule, value, callback) => {
            if (value === '') {
                callback(new Error('请再次输入密码'));
            } else if (value !== this.registerForm.password) {
                callback(new Error('两次输入密码不一致!'));
            } else {
                callback();
            }
        }
        return {
            registerForm: {
                username: '',
                email: '',
                verifycode: '',
                password: '',
                checkpassword: ''
            },

            loginRules: {
                username: [
                    { required: true, message: '用户名不能为空', trigger: 'blur' },
                    { min: 3, max: 50, message: '长度必须为3-50个字符', trigger: 'blur' },
                    { pattern: /^\w+$/, message: '只能包含字母/数字/下划线', trigger: 'blur' },
                ],
                email: [
                    { required: true, message: '邮箱不能为空', trigger: 'blur' },
                    { pattern: /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/, message: '邮箱格式错误', trigger: 'blur' },

                ],
                verifycode: [
                    { required: true, message: '请输入验证码', trigger: 'blur' }
                ],
                password: [
                    { required: true, message: '请输入密码', trigger: 'blur' },
                    { min: 6, message: '长度至少6个字符', trigger: 'blur' }
                ],
                checkpassword: [
                    { validator: validatePass2, trigger: 'blur' }
                ]
            },
            loading: false,
            loading2: false,
            passwordType: 'password',
            passwordType2: 'password',
            redirect: undefined
        }
    },
    watch: {
        $route: {
            handler: function (route) {
                this.redirect = route.query && route.query.redirect
            },
            immediate: true
        }
    },
    methods: {
        gotoLogin() {
            this.$router.push('/login')
        },
        showPwd() {
            if (this.passwordType === 'password') {
                this.passwordType = ''
            } else {
                this.passwordType = 'password'
            }
            this.$nextTick(() => {
                this.$refs.password.focus()
            })
        },
        showPwd2() {
            if (this.passwordType2 === 'password') {
                this.passwordType2 = ''
            } else {
                this.passwordType2 = 'password'
            }
            this.$nextTick(() => {
                this.$refs.password.focus()
            })
        },
        handleVerifyCode() {
            let hasError = false;
            this.$refs.registerForm.validateField(['username', 'email'], err => {
                if (err) {
                    hasError = true;
                    return;
                }
            });
            if (!hasError) {
                this.loading2 = true;
                sendVerifyCode(this.registerForm).then(() => {
                    this.$message('验证码发送成功')
                    this.loading2 = false
                }).catch(() => {
                    this.loading2 = false
                })
            }
        },
        handleRegister() {
            this.$refs.registerForm.validate(valid => {
                if (valid) {
                    this.loading = true
                    register(this.registerForm).then(() => {
                        this.$message('注册成功')
                        this.loading = false
                        this.$router.push('/login')
                    }).catch(() => {
                        this.loading = false
                    })
                } else {
                    console.log('error submit!!')
                    return false
                }
            })
        }
    }
}
</script>

<style lang="scss">
/* 修复input 背景不协调 和光标变色 */
/* Detail see https://github.com/PanJiaChen/vue-element-admin/pull/927 */

$bg: #283443;
$light_gray: #fff;
$cursor: #fff;

@supports (-webkit-mask: none) and (not (cater-color: $cursor)) {
    .login-container .el-input input {
        color: $cursor;
    }
}

/* reset element-ui css */
.login-container {
    .el-input {
        display: inline-block;
        height: 47px;
        width: 85%;

        input {
            background: transparent;
            border: 0px;
            -webkit-appearance: none;
            border-radius: 0px;
            padding: 12px 5px 12px 15px;
            color: $light_gray;
            height: 47px;
            caret-color: $cursor;

            &:-webkit-autofill {
                box-shadow: 0 0 0px 1000px $bg inset !important;
                -webkit-text-fill-color: $cursor !important;
            }
        }
    }

    .el-form-item {
        border: 1px solid rgba(255, 255, 255, 0.1);
        background: rgba(0, 0, 0, 0.1);
        border-radius: 5px;
        color: #454545;
    }
}
</style>

<style lang="scss" scoped>
$bg: #2d3a4b;
$dark_gray: #889aa4;
$light_gray: #eee;

.login-container {
    min-height: 100%;
    width: 100%;
    background-color: $bg;
    overflow: hidden;

    .login-form {
        position: relative;
        top: -40px;
        width: 520px;
        max-width: 100%;
        padding: 160px 35px 0;
        margin: 0 auto;
        overflow: hidden;
    }

    .tips {
        font-size: 14px;
        color: #fff;
        margin-bottom: 10px;

        span {
            &:first-of-type {
                margin-right: 16px;
            }
        }
    }

    .svg-container {
        padding: 6px 5px 6px 15px;
        color: $dark_gray;
        vertical-align: middle;
        width: 30px;
        display: inline-block;
    }

    .title-container {
        position: relative;

        .title {
            font-size: 26px;
            color: $light_gray;
            margin: 0px auto 40px auto;
            text-align: center;
            font-weight: bold;
        }
    }

    .show-pwd {
        position: absolute;
        right: 10px;
        top: 7px;
        font-size: 16px;
        color: $dark_gray;
        cursor: pointer;
        user-select: none;
    }
}
</style>
