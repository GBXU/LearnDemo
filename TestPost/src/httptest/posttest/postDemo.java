package httptest.posttest;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.HttpStatus;
import org.apache.http.NameValuePair;
import org.apache.http.client.CookieStore;
import org.apache.http.client.config.CookieSpecs;
import org.apache.http.client.config.RequestConfig;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClientBuilder;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.protocol.HTTP;





public class postDemo {
	public static void main(String[] arg){
		RequestConfig requestConfig = RequestConfig.custom().setCookieSpec(CookieSpecs.STANDARD_STRICT).build();
        CloseableHttpClient httpClient = HttpClients.custom().setDefaultRequestConfig(requestConfig).build();
/*
		String zhihu = "https://www.zhihu.com/#signin";
		String loginhtml = sendGet(zhihu, "utf-8");
		//<input type="hidden" name="_xsrf" value="a962963cb74300d254366ed738e5d017"/>
		String patIndexCode = "input type=\"hidden\" name=\"_xsrf\" value=\"(.+?)\"/>";
		String indexCode = "";
		Pattern pattern = Pattern.compile(patIndexCode);
		Matcher matcher = pattern.matcher(loginhtml);
		if(matcher.find()){
			indexCode = matcher.group(1);
		}
		//System.out.println(indexCode);

		//static final CookieStore cookieStore = null;
		String url = "https://www.zhihu.com/";

		//params.add(new BasicNameValuePair("zjh", "2014141462281"));
        //params.add(new BasicNameValuePair("mm", "111111qq"));

		List <NameValuePair> params = new ArrayList<NameValuePair>();  
		params.add(new BasicNameValuePair("_xsrf", indexCode));
		params.add(new BasicNameValuePair("password", "111111qq"));
        params.add(new BasicNameValuePair("email", "932739864@qq.com"));
        
        String html = sendPost(url, "utf-8", params);
        System.out.println(html);
*/

		String localurl = "http://localhost:8081/TestRoot/Login";
		List <NameValuePair> params = new ArrayList<NameValuePair>();  
		params.add(new BasicNameValuePair("EM", "xgb99@outlook.com"));
		params.add(new BasicNameValuePair("PW", "123"));
		String html = sendPost(localurl, "utf-8", params);
		System.out.println(html);
	}
	/**
	 * ��ȡҪץȡҳ�����������
	 * 
	 * @param url
	 *            ��ҳ��ַ
	 * @return
	 */
	public static String sendPost(String url, String format, List<NameValuePair> params) {
		BufferedReader in = null;
		String result = "";
		// ͨ��HttpClientBuilder����HttpClient
		HttpClientBuilder httpClientBuilder = HttpClientBuilder.create();
		CloseableHttpClient client = httpClientBuilder.build();
		
		//Post��������url��ַ
		HttpPost httpPost = new HttpPost(url);
		
		
		// ��������ʹ��䳬ʱʱ��
		RequestConfig requestConfig = RequestConfig.custom().setConnectTimeout(5000).build();
		//����HttpGet����
		httpPost.setConfig(requestConfig);
		//List <NameValuePair> params = new ArrayList<NameValuePair>();  
        //params.add(new BasicNameValuePair("user", "passwd")); 
        
        
		System.out.println(httpPost.getRequestLine());

		try {
			HttpEntity postEntity = new UrlEncodedFormEntity(params,"utf-8");
			httpPost.setEntity(postEntity);
			HttpResponse httpResponse = client.execute(httpPost);

			int statusCode = httpResponse.getStatusLine().getStatusCode();

			// ��Ӧ״̬
			System.out.println("status:" + statusCode);
			if (statusCode == HttpStatus.SC_OK) {
				// ��ȡ��Ӧ����Ϣʵ��
				HttpEntity entity = httpResponse.getEntity();

				// �ж�ʵ���Ƿ�Ϊ��
				if (entity != null) {
					System.out.println("contentEncoding:" + entity.getContentLength());

					in = new BufferedReader(new InputStreamReader(
							entity.getContent(), format));

					String line;
					while ((line = in.readLine()) != null) {
						// ����ץȡ����ÿһ�в�����洢��result����
						result += line;
					}
				}
			}
		} catch (Exception e) {
			e.printStackTrace();
		} finally {
			try {
				client.close();
				if (in != null) {
					in.close();
				}
			} catch (Exception e2) {
				e2.printStackTrace();
			}
		}
		return result;
	}
	
	public static String sendGet(String url, String format) {

		BufferedReader in = null;
		String result = "";
		// ͨ��HttpClientBuilder����HttpClient
		HttpClientBuilder httpClientBuilder = HttpClientBuilder.create();
		CloseableHttpClient client = httpClientBuilder.build();
		
		//Get��������url��ַ
		HttpGet httpGet = new HttpGet(url);
		
		// ��������ʹ��䳬ʱʱ��
		RequestConfig requestConfig = RequestConfig.custom()
				.setConnectTimeout(5000).build();
		//����HttpGet����
		httpGet.setConfig(requestConfig);

		System.out.println(httpGet.getRequestLine());

		try {
			HttpResponse httpResponse = client.execute(httpGet);

			int statusCode = httpResponse.getStatusLine().getStatusCode();

			// ��Ӧ״̬
			System.out.println("status:" + statusCode);
			if (statusCode == HttpStatus.SC_OK) {
				// ��ȡ��Ӧ����Ϣʵ��
				HttpEntity entity = httpResponse.getEntity();

				// �ж�ʵ���Ƿ�Ϊ��
				if (entity != null) {
					System.out.println("contentEncoding:"
							+ entity.getContentLength());

					in = new BufferedReader(new InputStreamReader(
							entity.getContent(), format));

					String line;
					while ((line = in.readLine()) != null) {
						// ����ץȡ����ÿһ�в�����洢��result����
						result += line;
					}
				}
			}
		} catch (Exception e) {
			e.printStackTrace();
		} finally {
			try {
				client.close();
				if (in != null) {
					in.close();
				}
			} catch (Exception e2) {
				e2.printStackTrace();
			}
		}
		return result;
	}

}
