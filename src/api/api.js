import axios from 'axios';

let base = 'http://127.0.0.1:5000/api';

export const requestLogin = params => {
    return axios({
        method: 'POST',
        url: `${base}/login`,
        auth: params
    })
    .then(res => res.data);
};

export const setpwd = params => {
    return axios.post(`${base}/setpwd`, params);
};

export const getUserListPage = params => {
    return axios.get(`${base}/users/listpage`, { params: params });
};

export const removeUser = params => {
    return axios.get(`${base}/user/remove`, { params: params });
};

export const batchRemoveUser = params => {
    return axios.get(`${base}/user/bathremove`, { params: params });
};

export const getdrawPieChart = () => {
    return axios.get(`${base}/getdrawPieChart`);
};

export const getdrawLineChart = () => {
    return axios.get(`${base}/getdrawLineChart`);
};

export const exp_excel = () => {
    return axios.get(`${base}/exp_excel`);
};

export const getdrawStackedAreaChart = () => {
    return axios.get(`${base}/getdrawStackedAreaChart`);
    //todo
};

export const getdrawAirClogChart = () => {
    return axios.get(`${base}/getdrawAirClogChart`);
};

export const getdrawSizeNH3Chart = () => {
    return axios.get(`${base}/getdrawSizeNH3Chart`);
};

export const getdrawAirDeposiChart = () => {
    return axios.get(`${base}/getdrawAirDeposiChart`);
};