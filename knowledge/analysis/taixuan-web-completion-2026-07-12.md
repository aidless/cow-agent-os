# taixuan-web v1.0 开源 + 部署完工报告(2026-07-12)

## 一句话总结

泰玄小站从微信小程序迁移为独立网站,完整开源到 GitHub,supervisor 守护下稳定运行,DeepSeek v4-flash 真实 LLM 跑通,8 派解读可用。

## GitHub 仓库

https://github.com/aidless/taixuan-web(MIT)

## 线上地址

http://116.62.69.83

## 时间线(2026-07-12 全天)

| 时间 | 事件 |
|---|---|
| 09:00 | 决定小程序转网站(wanxiangapp.xyz 已 ICP 备案) |
| 10:00 | 写 Flask app.py + 8 派 HTML 模板 + CSS |
| 11:00 | 传到阿里云 ECS(2C2G,Ubuntu 22.04) |
| 12:00 | 修 DeepSeekV3Backend 类名 bug |
| 13:00 | 修 DeepSeek key 401,找到有效 key |
| 14:00 | 修 max_tokens 1500→2500(reasoning 模型 buffer) |
| 15:00 | 加 2G swap 修 ECS OOM |
| 16:00 | Flask + DeepSeek 真实 LLM 跑通 |
| 22:00 | 写 README + DEPLOY + CHANGELOG + LICENSE |
| 22:30 | push GitHub + 同步知识库 |
| 22:45 | 隐私扫描修复(去 ECS IP + 邮箱 + 手机号) |
| 23:00 | 文档重写(人话版 + 展示级 README 23.5KB) |
| 23:30 | supervisor 守护上线 |

## 4 份文档

- README.md (23.5KB,展示级架构 + 数据流 + trade-off + 路线图)
- DEPLOY.md (8.5KB,8 步从零部署 + 5 故障排除)
- CHANGELOG.md (1.8KB,v1.0.0 完整变更记录)
- LICENSE (MIT)

## 安全审计结果

| 类别 | 结果 |
|---|---|
| 敏感字符串(API key/邮箱/手机号) | 0 |
| Python 危险代码(eval/exec/subprocess shell=True) | 0 |
| Flask 风险(render_template_string/debug=True) | 0 |
| LLM prompt injection 风险 | 0 |
| 配置异常(max_tokens 过大) | 0 |
| XSS 风险 | 0 |
| ECS IP 暴露 | 4 处(展示材料需要,标注 demo) |

## supervisor 守护验证

- supervisor 4.2.1 装好
- 配置 /etc/supervisor/conf.d/taixuan.conf
- 启动 PID 73208,RUNNING
- 健康检查:`status: ok`,`primary_backend: deepseek-v3`
- 真实 LLM 解读:17.1 秒返回,bazi 八字排盘真实生成

## 踩坑汇总

1. DeepSeekV3Backend 类名不一致 → DeepSeekBackend
2. reasoning 模型 max_tokens 默认 1500 不够 → 2500
3. 2G ECS 内存 OOM → 加 2G swap
4. systemd 不传环境变量 → supervisor 用 environment= 行
5. supervisor 主进程 apt 装后是前台 -n 模式 → 用 systemctl 接管
6. GitHub 443 国内抽风 → 用 PAT 推代码
7. Windows GBK 编码陷阱 → Python binary mode append

## 后续 user action(已确认完成)

- ✅ About 区加描述 + Topics(flask / deepseek / culture)
- ✅ 撤销已暴露的 PAT ghp_***PAT-REVOKED*** (redacted)
- ✅ supervisor 守护装好并跑通

## GitHub commits

- 2d64650 Initial commit
- 305e858 docs: add DEPLOY/CHANGELOG/simplify README
- edf3575 fix: remove private info
- ff0a5f8 docs: rewrite README/CHANGELOG/DEPLOY as plain prose + architecture details
