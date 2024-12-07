<template>
    <div class="app-container">
        <h2 class="title" style="text-align: center;">管理员失物列表</h2>
        <el-form :inline=true>
            <el-form-item label="物品:">
                <el-input v-model="search" placeholder="搜索失物..." @keydown.enter.native="handleSearch" class="input" />
            </el-form-item>
            <el-form-item label="类别:">
                <el-select v-model="category" placeholder="请选择类别" @change="fetchItems">
                    <el-option value="" label="所有类别" />
                    <el-option value="雨伞" label="雨伞" />
                    <el-option value="水杯" label="水杯" />
                    <el-option value="包" label="包" />
                    <el-option value="眼镜" label="眼镜" />
                    <el-option value="手机" label="手机" />
                    <el-option value="电脑" label="电脑" />
                    <el-option value="其它" label="其它" />
                </el-select>
            </el-form-item>
            <el-form-item label="状态:">
                <el-select v-model="claimedStatus" placeholder="请选择状态" @change="fetchItems">
                    <el-option value="" label="全部" />
                    <el-option value="claimed" label="已认领" />
                    <el-option value="unclaimed" label="未认领" />
                </el-select>
            </el-form-item>
        </el-form>
        <el-table v-loading="listLoading" :data="items" element-loading-text="Loading" border fit highlight-current-row
            :default-sort="{ prop: 'time', order: 'descending' }">
            <el-table-column align="center" label="编号" width="95">
                <template slot-scope="scope">
                    #{{ scope.row.id }}
                </template>
            </el-table-column>
            <el-table-column label="物品" align="center">
                <template slot-scope="scope">
                    <el-button type="text" @click="showDescription(scope.row.description, scope.row.id)"> <span style="
            text-decoration: underline;">{{ scope.row.item_name }}</span></el-button>
                </template>
            </el-table-column>
            <el-table-column label="类别" align="center">
                <template slot-scope="scope" align="center">
                    <span>{{ scope.row.category }}</span>
                </template>
            </el-table-column>
            <el-table-column label="拾得地点" width="110" align="center">
                <template slot-scope="scope">
                    {{ scope.row.location }}
                </template>
            </el-table-column>
            <el-table-column align="center" prop="time" label="拾得时间" sortable>
                <template slot-scope="scope">
                    <i class="el-icon-time" />
                    <span>{{ scope.row.found_date }}</span>
                </template>
            </el-table-column>
            <el-table-column label="上传用户" align="center">
                <template slot-scope="scope">
                    <el-button type="text" @click="showContactInfo(scope.row.upload_user, scope.row.contact_info)">
                        <span style="
            text-decoration: underline;">{{ scope.row.upload_user
                            }}</span></el-button>
                </template>
            </el-table-column>
            <el-table-column class-name="status-col" label="状态" align="center">
                <template slot-scope="scope">
                    <el-tag :type="scope.row.claimed | statusFilter">{{ scope.row.claimed ? '已认领' : '未认领' }}</el-tag>
                </template>
            </el-table-column>
            <el-table-column label="认领用户" align="center">
                <template slot-scope="scope">
                    <span>{{ scope.row.claimed_user || '--' }}</span>
                </template>
            </el-table-column>
            <el-table-column label="操作" align="center">
                <template slot-scope="scope">
                    <el-button type="danger" size="small"
                        @click="DeleteItem(scope.row.id, scope.row.item_name, scope.row.category, scope.row.claimed, scope.row.claimed_user, scope.row.upload_user)">
                        删除失物
                    </el-button>
                </template>
            </el-table-column>
        </el-table>
        <!-- 用户详细信息对话框 -->
        <el-dialog :visible.sync="modalVisible" title="上传用户信息">
            <p><strong>上传用户:</strong> {{ modalUser }}</p>
            <p><strong>联系方式:</strong> {{ modalContact }}</p>
            <span slot="footer" class="dialog-footer">
                <el-button type="primary" @click="closeModal">关 闭</el-button>
            </span>
        </el-dialog>


        <!-- 物品描述信息对话框 -->
        <el-dialog :visible.sync="tooltipVisible" title="物品描述信息">
            <p><strong>物品描述:</strong> {{ tooltipContent }}</p>
            <img :src="image_url" style="width: 100%;">
            <span slot="footer" class="dialog-footer">
                <el-button type="primary" @click="hideDescription">关 闭</el-button>
            </span>
        </el-dialog>

        <el-dialog :visible.sync="delete_modalVisible" title="是否删除失物信息?" @close="closeDeleteModal(false)">
            <p><strong>失物编号:</strong>{{ delete_item_id }}</p>
            <p><strong>失物名称:</strong>{{ delete_item_name }}</p>
            <p><strong>失物类别:</strong>{{ delete_item_category }}</p>
            <p><strong>上传用户:</strong>{{ delete_item_upload_user }}</p>
            <p><strong>认领状态:</strong>{{ delete_item_claimed }}</p>
            <p><strong>认领用户:</strong>{{ delete_item_claimed_user }}</p>
            <span slot="footer" class="dialog-footer">
                <el-button type="primary" @click="closeDeleteModal(true)">确 认</el-button>
                <el-button type="primary" @click="closeDeleteModal(false)">取 消</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
import { getItems } from '@/api/table'
import { deleteItem } from '@/api/table'
import { Message } from 'element-ui'
// import _ from 'lodash';
export default {
    filters: {
        statusFilter(status) {
            if (status) {
                return 'success'
            }
            return ''
        }
    },
    data() {
        return {
            results: [],
            listLoading: true,
            items: [],
            category: '',
            search: '',
            claimedStatus: '',
            tooltipVisible: false,
            tooltipContent: '',
            tooltipStyle: {},
            modalVisible: false,
            modalUser: '',
            modalContact: '',
            sortOrder: 'asc', // 排序方式，默认为升序
            image_url: process.env.VUE_APP_BASE_API + '/images/upload',
            delete_modalVisible: false,
            delete_item_id: '',
            delete_item_name: '',
            delete_item_category: '',
            delete_item_upload_user: '',
            delete_item_claimed: '',
            delete_item_claimed_user: '',
            delete_item_description: '',
        };
    },
    methods: {
        fetchItems() {
            console.log('排序方式值值:', this.sortOrder);
            getItems({
                category: this.category,
                search: this.search.trim(),
                claimed: this.claimedStatus,
                sort: this.sortOrder
            }).then(response => {
                this.items = response.data;
                this.listLoading = false;
            })
                .catch(error => {
                    console.error('获取失物列表失败:', error);
                });
        },
        // createFilter(queryString) {
        //   return (items) => {
        //     return _.includes(items.item_name, queryString);
        //   };
        // }
        handleSearch() {
            this.fetchItems();
            this.search = '';
        },
        showDescription(description, id) {
            this.tooltipVisible = true;
            this.image_url = process.env.VUE_APP_BASE_API + '/images/get/' + id;
            this.tooltipContent = description || '无描述';
        },
        hideDescription() {
            this.tooltipVisible = false;
        },
        showContactInfo(user, contact) {
            this.modalUser = user;
            this.modalContact = contact || '无';
            this.modalVisible = true;
        },
        closeModal() {
            this.modalVisible = false;
        },
        toggleSortOrder() {
            // 切换排序方式
            this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc';
            this.fetchItems();
        },
        DeleteItem(id, name, category, claimed, claimed_user, upload_user) {
            this.delete_modalVisible = true
            this.delete_item_id = id
            this.delete_item_name = name
            this.delete_item_category = category
            this.delete_item_upload_user = upload_user
            this.delete_item_claimed = claimed ? '已认领' : '未认领'
            this.delete_item_claimed_user = claimed_user || '无'
        },
        closeDeleteModal(confirmed) {
            this.delete_modalVisible = false
            if (confirmed) {
                deleteItem(this.delete_item_id)
                    .then((response) => {
                        console.log(11)
                        Message({
                            type: 'success',
                            message: '删除成功'
                        })
                        this.fetchItems()
                    })
                    .catch(error => {
                        console.error('删除失物失败:', error)
                    })
            }
        },
    },
    mounted() {
        this.fetchItems();
    },

};
</script>
<style scoped>
/* 整体样式 */
</style>
