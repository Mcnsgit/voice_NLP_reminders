
import { View,  ViewProps } from 'react-native';

import { useThemeColor } from '@/hooks/useThemeColor';

// const ThemedViewProps   {
//   lightColor = string;
//   darkColor?: string;
// };

export function ThemedView({ style, lightColor, darkColor, ...otherProps }) {
  const backgroundColor = useThemeColor({ light: lightColor, dark: darkColor }, 'background');

  return <View style={[{ backgroundColor }, style]} {...otherProps} />;
}
