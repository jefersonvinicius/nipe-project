# Projeto NIPE

## Leia o artigo em [aqui](results/article.pdf)

### Como configurar câmera do android? :camera:

No arquivo `.buildozer\android\platform\python-for-android\pythonforandroid\bootstraps\sdl2\build\templates\AndroidManifest.tmpl.xml` adicione os seguintes trechos de códigos:

```xml
...
<!-- Android 2.3.3 -->
<uses-sdk  android:minSdkVersion="{{ args.min_sdk_version }}"  android:targetSdkVersion="{{ android_api }}"  />

+ <uses-feature  android:name="android.hardware.camera"  />
+ <uses-feature  android:name="android.hardware.camera.autofocus"  />

<!-- OpenGL ES 2.0 -->
<uses-feature  android:glEsVersion="0x00020000"  />
...
```
```xml
	...
	<activity  android:name="{{ a }}"></activity>
	{% endfor %}
+		<provider
+			android:name="android.support.v4.content.FileProvider"
+			android:authorities="<Seu package name>"
+			android:exported="false"
+			android:grantUriPermissions="true">
+		<meta-data
+			android:name="android.support.FILE_PROVIDER_PATHS"
+			android:resource="@xml/file_paths"/>
+		</provider>
	</application>
</manifest>
```
**OBS**: em `<Seu package name>` você deve colocar o package completo do app. Ele é o `package.domain` concatenado com `package.name` fornecidos no `buildozer.spec`.
*Exemplo:*
```
# (str) Package name
package.name = marker

# (str) Package domain (needed for android/ios packaging)
package.domain = com.jeferson.developer	
```
Resultado: `com.jeferson.developer.marker`

---

Depois, crie uma pasta chamada `xml` no diretório `.buildozer\android\platform\python-for-android\pythonforandroid\bootstraps\sdl2\build\src\main\res` e dentro dela crie um arquivo chamado `file_paths.xml` com o seguinte código:

```xml
<?xml version="1.0" encoding="utf-8"?>
<paths  xmlns:android="http://schemas.android.com/apk/res/android">
	<external-path  name="external_files"  path="Android/data/<Seu package name>/files/Pictures"  />
</paths>
```
**Não esqueça do package neste arquivo também!**
